import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    win_rate_risk: "low", erosion_pattern: "none",
    erosion_severity: "stable", recommended_action: "no_action",
    win_rate_decline_score: 0.0, deal_quality_score: 0.0,
    competitive_readiness_score: 0.0, pattern_intensity_score: 0.0,
    win_rate_composite: 0.0, is_win_rate_eroding: false, requires_coaching: false,
    estimated_lost_revenue_usd: 0.0,
    erosion_signal: "Win rate stable — above benchmark — no erosion signals detected",
  },
  {
    rep_id: "rep_002", region: "East",
    win_rate_risk: "low", erosion_pattern: "pricing_displacement",
    erosion_severity: "stable", recommended_action: "no_action",
    win_rate_decline_score: 8.0, deal_quality_score: 6.0,
    competitive_readiness_score: 5.0, pattern_intensity_score: 4.0,
    win_rate_composite: 6.3, is_win_rate_eroding: false, requires_coaching: false,
    estimated_lost_revenue_usd: 3780.0,
    erosion_signal: "Win rate 54% vs 55% prior — 3 price losses — composite 6",
  },
  {
    rep_id: "rep_003", region: "Central",
    win_rate_risk: "moderate", erosion_pattern: "rep_skill_gap",
    erosion_severity: "declining", recommended_action: "battlecard_refresh",
    win_rate_decline_score: 22.0, deal_quality_score: 18.0,
    competitive_readiness_score: 20.0, pattern_intensity_score: 12.0,
    win_rate_composite: 18.9, is_win_rate_eroding: false, requires_coaching: false,
    estimated_lost_revenue_usd: 28350.0,
    erosion_signal: "Win rate 48% vs 55% prior — late stage loss rate 40% — composite 19",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    win_rate_risk: "moderate", erosion_pattern: "feature_regression",
    erosion_severity: "declining", recommended_action: "competitive_coaching",
    win_rate_decline_score: 28.0, deal_quality_score: 25.0,
    competitive_readiness_score: 22.0, pattern_intensity_score: 18.0,
    win_rate_composite: 24.3, is_win_rate_eroding: false, requires_coaching: false,
    estimated_lost_revenue_usd: 60750.0,
    erosion_signal: "Win rate 42% vs 54% prior — 4 feature gap losses — battlecard 95 days old — composite 24",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    win_rate_risk: "high", erosion_pattern: "champion_poaching",
    erosion_severity: "eroding", recommended_action: "competitive_coaching",
    win_rate_decline_score: 42.0, deal_quality_score: 35.0,
    competitive_readiness_score: 38.0, pattern_intensity_score: 28.0,
    win_rate_composite: 36.8, is_win_rate_eroding: false, requires_coaching: true,
    estimated_lost_revenue_usd: 147200.0,
    erosion_signal: "Win rate 38% vs 55% prior — 2 champions poached — late stage 50% loss — composite 37",
  },
  {
    rep_id: "rep_006", region: "West",
    win_rate_risk: "high", erosion_pattern: "pricing_displacement",
    erosion_severity: "eroding", recommended_action: "pricing_strategy_review",
    win_rate_decline_score: 45.0, deal_quality_score: 30.0,
    competitive_readiness_score: 35.0, pattern_intensity_score: 32.0,
    win_rate_composite: 37.3, is_win_rate_eroding: false, requires_coaching: true,
    estimated_lost_revenue_usd: 186500.0,
    erosion_signal: "Win rate 35% vs 58% prior — 8 price losses — competitor strength 72 — composite 37",
  },
  {
    rep_id: "rep_007", region: "APAC",
    win_rate_risk: "critical", erosion_pattern: "systematic_loss",
    erosion_severity: "collapse", recommended_action: "executive_competitive_review",
    win_rate_decline_score: 72.0, deal_quality_score: 65.0,
    competitive_readiness_score: 68.0, pattern_intensity_score: 58.0,
    win_rate_composite: 66.8, is_win_rate_eroding: true, requires_coaching: true,
    estimated_lost_revenue_usd: 502000.0,
    erosion_signal: "Win rate 22% vs 58% prior — 6 consecutive losses — -20pp 3-period trend — composite 67",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    win_rate_risk: "critical", erosion_pattern: "systematic_loss",
    erosion_severity: "collapse", recommended_action: "executive_competitive_review",
    win_rate_decline_score: 80.0, deal_quality_score: 75.0,
    competitive_readiness_score: 78.0, pattern_intensity_score: 70.0,
    win_rate_composite: 76.1, is_win_rate_eroding: true, requires_coaching: true,
    estimated_lost_revenue_usd: 760000.0,
    erosion_signal: "Win rate 18% vs 62% prior — 8 consecutive losses — late stage 78% loss — composite 76",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-competitive-win-rate-erosion-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.win_rate_risk     === risk);
  if (pattern) reps = reps.filter((r) => r.erosion_pattern   === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_dec = 0, total_qual = 0, total_read = 0, total_pat = 0, total_rev = 0;

  for (const r of mockReps) {
    risk_counts[r.win_rate_risk]       = (risk_counts[r.win_rate_risk] || 0) + 1;
    pattern_counts[r.erosion_pattern]  = (pattern_counts[r.erosion_pattern] || 0) + 1;
    severity_counts[r.erosion_severity] = (severity_counts[r.erosion_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.win_rate_composite;
    total_dec  += r.win_rate_decline_score;
    total_qual += r.deal_quality_score;
    total_read += r.competitive_readiness_score;
    total_pat  += r.pattern_intensity_score;
    total_rev  += r.estimated_lost_revenue_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                            n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_win_rate_composite:           Math.round((total_comp / n) * 10) / 10,
      eroding_count:                    mockReps.filter((r) => r.is_win_rate_eroding).length,
      coaching_count:                   mockReps.filter((r) => r.requires_coaching).length,
      avg_win_rate_decline_score:       Math.round((total_dec  / n) * 10) / 10,
      avg_deal_quality_score:           Math.round((total_qual / n) * 10) / 10,
      avg_competitive_readiness_score:  Math.round((total_read / n) * 10) / 10,
      avg_pattern_intensity_score:      Math.round((total_pat  / n) * 10) / 10,
      total_estimated_lost_revenue_usd: Math.round(total_rev * 100) / 100,
    },
  });
}
