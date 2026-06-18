import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "REP-001", region: "West",
    value_risk: "low", value_pattern: "none",
    value_severity: "compelling", recommended_action: "no_action",
    message_quality_score: 5.0, value_defense_score: 5.0,
    proof_score: 5.0, deal_economics_score: 5.0,
    value_composite: 5.0,
    has_value_gap: false, requires_value_coaching: true,
    estimated_lost_revenue_usd: 0.0,
    value_signal: "Value proposition strong — message consistency, ROI quantification, proof strategy, and deal economics within benchmarks",
  },
  {
    rep_id: "REP-002", region: "East",
    value_risk: "low", value_pattern: "none",
    value_severity: "compelling", recommended_action: "no_action",
    message_quality_score: 8.0, value_defense_score: 7.0,
    proof_score: 9.0, deal_economics_score: 6.0,
    value_composite: 7.65,
    has_value_gap: false, requires_value_coaching: true,
    estimated_lost_revenue_usd: 8000.0,
    value_signal: "Value proposition strong — message consistency, ROI quantification, proof strategy, and deal economics within benchmarks",
  },
  {
    rep_id: "REP-003", region: "Central",
    value_risk: "moderate", value_pattern: "none",
    value_severity: "adequate", recommended_action: "value_message_refresh",
    message_quality_score: 20.0, value_defense_score: 18.0,
    proof_score: 22.0, deal_economics_score: 15.0,
    value_composite: 19.25,
    has_value_gap: false, requires_value_coaching: true,
    estimated_lost_revenue_usd: 30000.0,
    value_signal: "None — 22% pricing objections — 25% deals discounted to close — 55% with quantified ROI — composite 19",
  },
  {
    rep_id: "REP-004", region: "Northeast",
    value_risk: "moderate", value_pattern: "roi_ambiguity",
    value_severity: "adequate", recommended_action: "value_message_refresh",
    message_quality_score: 22.0, value_defense_score: 28.0,
    proof_score: 25.0, deal_economics_score: 18.0,
    value_composite: 23.95,
    has_value_gap: false, requires_value_coaching: true,
    estimated_lost_revenue_usd: 55000.0,
    value_signal: "ROI ambiguity — 28% pricing objections — 28% deals discounted to close — 40% with quantified ROI — composite 24",
  },
  {
    rep_id: "REP-005", region: "Southeast",
    value_risk: "high", value_pattern: "proof_dependent",
    value_severity: "deteriorating", recommended_action: "proof_strategy_coaching",
    message_quality_score: 35.0, value_defense_score: 32.0,
    proof_score: 45.0, deal_economics_score: 28.0,
    value_composite: 36.2,
    has_value_gap: true, requires_value_coaching: true,
    estimated_lost_revenue_usd: 120000.0,
    value_signal: "Proof dependent — 35% pricing objections — 38% deals discounted to close — 30% with quantified ROI — composite 36",
  },
  {
    rep_id: "REP-006", region: "West",
    value_risk: "high", value_pattern: "price_before_value",
    value_severity: "deteriorating", recommended_action: "roi_quantification_coaching",
    message_quality_score: 42.0, value_defense_score: 45.0,
    proof_score: 35.0, deal_economics_score: 48.0,
    value_composite: 42.45,
    has_value_gap: true, requires_value_coaching: true,
    estimated_lost_revenue_usd: 200000.0,
    value_signal: "Price before value — 45% pricing objections — 48% deals discounted to close — 25% with quantified ROI — composite 42",
  },
  {
    rep_id: "REP-007", region: "APAC",
    value_risk: "critical", value_pattern: "value_vacuum",
    value_severity: "failing", recommended_action: "commercial_reset",
    message_quality_score: 68.0, value_defense_score: 62.0,
    proof_score: 58.0, deal_economics_score: 60.0,
    value_composite: 63.2,
    has_value_gap: true, requires_value_coaching: true,
    estimated_lost_revenue_usd: 450000.0,
    value_signal: "Value vacuum — 62% pricing objections — 65% deals discounted to close — 12% with quantified ROI — composite 63",
  },
  {
    rep_id: "REP-008", region: "EMEA",
    value_risk: "critical", value_pattern: "executive_disconnect",
    value_severity: "failing", recommended_action: "value_repositioning_program",
    message_quality_score: 78.0, value_defense_score: 72.0,
    proof_score: 68.0, deal_economics_score: 70.0,
    value_composite: 73.1,
    has_value_gap: true, requires_value_coaching: true,
    estimated_lost_revenue_usd: 680000.0,
    value_signal: "Executive disconnect — 72% pricing objections — 72% deals discounted to close — 10% with quantified ROI — composite 73",
  },
];

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/api/sales-value-proposition-deterioration-intelligence-engine`, { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_m = 0, total_v = 0, total_p = 0, total_d = 0, total_lr = 0;

  for (const r of mockReps) {
    risk_counts[r.value_risk]       = (risk_counts[r.value_risk] || 0) + 1;
    pattern_counts[r.value_pattern] = (pattern_counts[r.value_pattern] || 0) + 1;
    severity_counts[r.value_severity] = (severity_counts[r.value_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.value_composite;
    total_m    += r.message_quality_score;
    total_v    += r.value_defense_score;
    total_p    += r.proof_score;
    total_d    += r.deal_economics_score;
    total_lr   += r.estimated_lost_revenue_usd;
  }

  const n = mockReps.length;
  return NextResponse.json({
    reps: mockReps,
    summary: {
      total:                                n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_value_composite:                  Math.round((total_comp / n) * 10) / 10,
      value_gap_count:                      mockReps.filter((r) => r.has_value_gap).length,
      coaching_count:                       mockReps.filter((r) => r.requires_value_coaching).length,
      avg_message_quality_score:            Math.round((total_m / n) * 10) / 10,
      avg_value_defense_score:              Math.round((total_v / n) * 10) / 10,
      avg_proof_score:                      Math.round((total_p / n) * 10) / 10,
      avg_deal_economics_score:             Math.round((total_d / n) * 10) / 10,
      total_estimated_lost_revenue_usd:     Math.round(total_lr * 100) / 100,
    },
  });
}
