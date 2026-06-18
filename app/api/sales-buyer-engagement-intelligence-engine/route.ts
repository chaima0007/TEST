import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    engagement_risk: "low", engagement_pattern: "none",
    engagement_severity: "engaged", recommended_action: "no_action",
    responsiveness_score: 0.0, signal_score: 0.0,
    activation_score: 0.0, risk_score: 0.0,
    engagement_composite: 0.0,
    has_engagement_gap: false, requires_engagement_coaching: false,
    estimated_revenue_at_dark_usd: 0.0,
    engagement_signal: "Buyer engagement strong — response rates, signal quality, and deal activation within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    engagement_risk: "low", engagement_pattern: "none",
    engagement_severity: "engaged", recommended_action: "no_action",
    responsiveness_score: 4.0, signal_score: 3.0,
    activation_score: 5.0, risk_score: 2.0,
    engagement_composite: 3.65,
    has_engagement_gap: false, requires_engagement_coaching: false,
    estimated_revenue_at_dark_usd: 0.0,
    engagement_signal: "Buyer engagement strong — response rates, signal quality, and deal activation within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    engagement_risk: "moderate", engagement_pattern: "proposal_black_hole",
    engagement_severity: "responsive", recommended_action: "engagement_quality_coaching",
    responsiveness_score: 20.0, signal_score: 22.0,
    activation_score: 18.0, risk_score: 15.0,
    engagement_composite: 19.55,
    has_engagement_gap: true, requires_engagement_coaching: true,
    estimated_revenue_at_dark_usd: 54000.0,
    engagement_signal: "Proposal black hole — 42% buyer email response — 70% meeting attendance — 12% deals gone dark — composite 20",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    engagement_risk: "moderate", engagement_pattern: "low_signal_pursuer",
    engagement_severity: "responsive", recommended_action: "engagement_quality_coaching",
    responsiveness_score: 22.0, signal_score: 28.0,
    activation_score: 18.0, risk_score: 12.0,
    engagement_composite: 21.3,
    has_engagement_gap: true, requires_engagement_coaching: true,
    estimated_revenue_at_dark_usd: 102000.0,
    engagement_signal: "Low signal pursuer — 38% buyer email response — 65% meeting attendance — 15% deals gone dark — composite 21",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    engagement_risk: "high", engagement_pattern: "meeting_canceler",
    engagement_severity: "passive", recommended_action: "buyer_activation_coaching",
    responsiveness_score: 40.0, signal_score: 38.0,
    activation_score: 42.0, risk_score: 35.0,
    engagement_composite: 39.25,
    has_engagement_gap: true, requires_engagement_coaching: true,
    estimated_revenue_at_dark_usd: 405000.0,
    engagement_signal: "Meeting canceler — 28% buyer email response — 50% meeting attendance — 28% deals gone dark — composite 39",
  },
  {
    rep_id: "rep_006", region: "West",
    engagement_risk: "high", engagement_pattern: "engagement_ignorer",
    engagement_severity: "passive", recommended_action: "engagement_quality_coaching",
    responsiveness_score: 48.0, signal_score: 45.0,
    activation_score: 40.0, risk_score: 50.0,
    engagement_composite: 45.55,
    has_engagement_gap: true, requires_engagement_coaching: true,
    estimated_revenue_at_dark_usd: 918000.0,
    engagement_signal: "Engagement ignorer — 22% buyer email response — 48% meeting attendance — 38% deals gone dark — composite 46",
  },
  {
    rep_id: "rep_007", region: "APAC",
    engagement_risk: "critical", engagement_pattern: "one_way_sender",
    engagement_severity: "dark", recommended_action: "deal_qualification_review",
    responsiveness_score: 72.0, signal_score: 68.0,
    activation_score: 65.0, risk_score: 70.0,
    engagement_composite: 69.05,
    has_engagement_gap: true, requires_engagement_coaching: true,
    estimated_revenue_at_dark_usd: 2160000.0,
    engagement_signal: "One-way sender — 12% buyer email response — 38% meeting attendance — 52% deals gone dark — composite 69",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    engagement_risk: "critical", engagement_pattern: "one_way_sender",
    engagement_severity: "dark", recommended_action: "deal_qualification_review",
    responsiveness_score: 100.0, signal_score: 100.0,
    activation_score: 100.0, risk_score: 100.0,
    engagement_composite: 100.0,
    has_engagement_gap: true, requires_engagement_coaching: true,
    estimated_revenue_at_dark_usd: 4050000.0,
    engagement_signal: "One-way sender — 10% buyer email response — 40% meeting attendance — 60% deals gone dark — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-buyer-engagement-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.engagement_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.engagement_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_rs = 0, total_ss = 0, total_ac = 0, total_rk = 0, total_dark = 0;

  for (const r of mockReps) {
    risk_counts[r.engagement_risk]       = (risk_counts[r.engagement_risk] || 0) + 1;
    pattern_counts[r.engagement_pattern] = (pattern_counts[r.engagement_pattern] || 0) + 1;
    severity_counts[r.engagement_severity] = (severity_counts[r.engagement_severity] || 0) + 1;
    action_counts[r.recommended_action]  = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.engagement_composite;
    total_rs   += r.responsiveness_score;
    total_ss   += r.signal_score;
    total_ac   += r.activation_score;
    total_rk   += r.risk_score;
    total_dark += r.estimated_revenue_at_dark_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                                   n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_engagement_composite:                Math.round((total_comp / n) * 10) / 10,
      engagement_gap_count:                    mockReps.filter((r) => r.has_engagement_gap).length,
      coaching_count:                          mockReps.filter((r) => r.requires_engagement_coaching).length,
      avg_responsiveness_score:                Math.round((total_rs / n) * 10) / 10,
      avg_signal_score:                        Math.round((total_ss / n) * 10) / 10,
      avg_activation_score:                    Math.round((total_ac / n) * 10) / 10,
      avg_risk_score:                          Math.round((total_rk / n) * 10) / 10,
      total_estimated_revenue_at_dark_usd:     Math.round(total_dark * 100) / 100,
    },
  });
}
