import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    competitive_risk: "low", competitive_pattern: "none",
    competitive_severity: "dominant", recommended_action: "no_action",
    win_rate_score: 0.0, competitive_intel_score: 0.0,
    deal_quality_score: 0.0, competitive_resilience_score: 0.0,
    competitive_effectiveness_composite: 0.0,
    is_competitive_threat: false, requires_competitive_coaching: false,
    estimated_revenue_at_risk_usd: 0.0,
    competitive_signal: "Competitive win rates strong across all deal segments",
  },
  {
    rep_id: "rep_002", region: "East",
    competitive_risk: "low", competitive_pattern: "none",
    competitive_severity: "dominant", recommended_action: "no_action",
    win_rate_score: 5.0, competitive_intel_score: 8.0,
    deal_quality_score: 5.0, competitive_resilience_score: 0.0,
    competitive_effectiveness_composite: 5.0,
    is_competitive_threat: false, requires_competitive_coaching: false,
    estimated_revenue_at_risk_usd: 0.0,
    competitive_signal: "Competitive win rates strong across all deal segments",
  },
  {
    rep_id: "rep_003", region: "Central",
    competitive_risk: "moderate", competitive_pattern: "no_competitive_intel",
    competitive_severity: "competitive", recommended_action: "competitive_training",
    win_rate_score: 10.0, competitive_intel_score: 30.0,
    deal_quality_score: 15.0, competitive_resilience_score: 10.0,
    competitive_effectiveness_composite: 16.5,
    is_competitive_threat: false, requires_competitive_coaching: true,
    estimated_revenue_at_risk_usd: 7200.0,
    competitive_signal: "No competitive intel — 44% win rate — 4 competitive losses — composite 17",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    competitive_risk: "moderate", competitive_pattern: "price_driven_loss",
    competitive_severity: "competitive", recommended_action: "competitive_training",
    win_rate_score: 10.0, competitive_intel_score: 15.0,
    deal_quality_score: 30.0, competitive_resilience_score: 15.0,
    competitive_effectiveness_composite: 17.75,
    is_competitive_threat: false, requires_competitive_coaching: true,
    estimated_revenue_at_risk_usd: 14400.0,
    competitive_signal: "Price driven loss — 40% win rate — 6 competitive losses — composite 18",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    competitive_risk: "high", competitive_pattern: "high_loss_rate",
    competitive_severity: "challenged", recommended_action: "deal_coaching",
    win_rate_score: 35.0, competitive_intel_score: 25.0,
    deal_quality_score: 28.0, competitive_resilience_score: 20.0,
    competitive_effectiveness_composite: 28.35,
    is_competitive_threat: false, requires_competitive_coaching: true,
    estimated_revenue_at_risk_usd: 36000.0,
    competitive_signal: "High loss rate — 33% win rate — 8 competitive losses — composite 28",
  },
  {
    rep_id: "rep_006", region: "West",
    competitive_risk: "high", competitive_pattern: "feature_gap_loss",
    competitive_severity: "challenged", recommended_action: "product_feedback_escalation",
    win_rate_score: 25.0, competitive_intel_score: 28.0,
    deal_quality_score: 38.0, competitive_resilience_score: 25.0,
    competitive_effectiveness_composite: 29.35,
    is_competitive_threat: false, requires_competitive_coaching: true,
    estimated_revenue_at_risk_usd: 54000.0,
    competitive_signal: "Feature gap loss — 35% win rate — 9 competitive losses — 2 displaced by competitor — composite 29",
  },
  {
    rep_id: "rep_007", region: "APAC",
    competitive_risk: "critical", competitive_pattern: "high_loss_rate",
    competitive_severity: "losing", recommended_action: "competitive_win_back",
    win_rate_score: 65.0, competitive_intel_score: 55.0,
    deal_quality_score: 50.0, competitive_resilience_score: 48.0,
    competitive_effectiveness_composite: 56.25,
    is_competitive_threat: true, requires_competitive_coaching: true,
    estimated_revenue_at_risk_usd: 180000.0,
    competitive_signal: "High loss rate — 22% win rate — 14 competitive losses — 4 displaced by competitor — composite 56",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    competitive_risk: "critical", competitive_pattern: "no_competitive_intel",
    competitive_severity: "losing", recommended_action: "competitive_training",
    win_rate_score: 70.0, competitive_intel_score: 65.0,
    deal_quality_score: 60.0, competitive_resilience_score: 58.0,
    competitive_effectiveness_composite: 64.35,
    is_competitive_threat: true, requires_competitive_coaching: true,
    estimated_revenue_at_risk_usd: 320000.0,
    competitive_signal: "No competitive intel — 18% win rate — 18 competitive losses — 6 displaced by competitor — composite 64",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-competitive-win-loss-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.competitive_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.competitive_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_wr = 0, total_intel = 0, total_dq = 0, total_res = 0, total_rev = 0;

  for (const r of mockReps) {
    risk_counts[r.competitive_risk]         = (risk_counts[r.competitive_risk] || 0) + 1;
    pattern_counts[r.competitive_pattern]   = (pattern_counts[r.competitive_pattern] || 0) + 1;
    severity_counts[r.competitive_severity] = (severity_counts[r.competitive_severity] || 0) + 1;
    action_counts[r.recommended_action]     = (action_counts[r.recommended_action] || 0) + 1;
    total_comp  += r.competitive_effectiveness_composite;
    total_wr    += r.win_rate_score;
    total_intel += r.competitive_intel_score;
    total_dq    += r.deal_quality_score;
    total_res   += r.competitive_resilience_score;
    total_rev   += r.estimated_revenue_at_risk_usd;
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
      avg_competitive_effectiveness_composite:  Math.round((total_comp / n) * 10) / 10,
      competitive_threat_count:                 mockReps.filter((r) => r.is_competitive_threat).length,
      competitive_coaching_count:               mockReps.filter((r) => r.requires_competitive_coaching).length,
      avg_win_rate_score:                       Math.round((total_wr / n) * 10) / 10,
      avg_competitive_intel_score:              Math.round((total_intel / n) * 10) / 10,
      avg_deal_quality_score:                   Math.round((total_dq / n) * 10) / 10,
      avg_competitive_resilience_score:         Math.round((total_res / n) * 10) / 10,
      total_estimated_revenue_at_risk_usd:      Math.round(total_rev * 100) / 100,
    },
  });
}
