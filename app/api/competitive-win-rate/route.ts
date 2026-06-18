import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockMatchups = [
  {
    matchup_id: "m_001", our_product: "ProductX", competitor: "CompetitorA",
    segment: "enterprise", region: "EMEA",
    win_rate_category: "strong", competitive_risk: "medium",
    trend_direction: "volatile", competitive_action: "reinforce",
    win_rate: 58.3, win_rate_delta: 6.3,
    deal_size_advantage: 1.18, cycle_efficiency: 1.26,
    champion_lift: 22.5, competitive_score: 63.8,
    is_at_risk: false, needs_battlecard: false,
    won_deals: 28, total_deals: 48,
  },
  {
    matchup_id: "m_002", our_product: "ProductX", competitor: "CompetitorB",
    segment: "mid-market", region: "NAMER",
    win_rate_category: "dominant", competitive_risk: "low",
    trend_direction: "improving", competitive_action: "leverage_strength",
    win_rate: 74.0, win_rate_delta: 12.0,
    deal_size_advantage: 1.35, cycle_efficiency: 1.42,
    champion_lift: 35.0, competitive_score: 82.5,
    is_at_risk: false, needs_battlecard: false,
    won_deals: 37, total_deals: 50,
  },
  {
    matchup_id: "m_003", our_product: "ProductY", competitor: "CompetitorA",
    segment: "smb", region: "APAC",
    win_rate_category: "competitive", competitive_risk: "medium",
    trend_direction: "stable", competitive_action: "differentiate",
    win_rate: 44.0, win_rate_delta: -2.0,
    deal_size_advantage: 0.95, cycle_efficiency: 1.08,
    champion_lift: 12.0, competitive_score: 48.2,
    is_at_risk: false, needs_battlecard: false,
    won_deals: 22, total_deals: 50,
  },
  {
    matchup_id: "m_004", our_product: "ProductY", competitor: "CompetitorC",
    segment: "enterprise", region: "NAMER",
    win_rate_category: "weak", competitive_risk: "high",
    trend_direction: "declining", competitive_action: "battlecard_update",
    win_rate: 32.0, win_rate_delta: -14.0,
    deal_size_advantage: 0.78, cycle_efficiency: 0.88,
    champion_lift: -8.0, competitive_score: 28.5,
    is_at_risk: true, needs_battlecard: true,
    won_deals: 16, total_deals: 50,
  },
  {
    matchup_id: "m_005", our_product: "ProductX", competitor: "CompetitorD",
    segment: "enterprise", region: "LATAM",
    win_rate_category: "critical", competitive_risk: "critical",
    trend_direction: "declining", competitive_action: "strategic_review",
    win_rate: 18.0, win_rate_delta: -22.0,
    deal_size_advantage: 0.62, cycle_efficiency: 0.72,
    champion_lift: -15.0, competitive_score: 14.2,
    is_at_risk: true, needs_battlecard: true,
    won_deals: 9, total_deals: 50,
  },
  {
    matchup_id: "m_006", our_product: "ProductZ", competitor: "CompetitorB",
    segment: "mid-market", region: "EMEA",
    win_rate_category: "strong", competitive_risk: "low",
    trend_direction: "improving", competitive_action: "reinforce",
    win_rate: 62.0, win_rate_delta: 9.0,
    deal_size_advantage: 1.22, cycle_efficiency: 1.18,
    champion_lift: 28.0, competitive_score: 68.4,
    is_at_risk: false, needs_battlecard: false,
    won_deals: 31, total_deals: 50,
  },
  {
    matchup_id: "m_007", our_product: "ProductZ", competitor: "CompetitorC",
    segment: "smb", region: "APAC",
    win_rate_category: "competitive", competitive_risk: "medium",
    trend_direction: "volatile", competitive_action: "differentiate",
    win_rate: 46.0, win_rate_delta: 4.0,
    deal_size_advantage: 1.05, cycle_efficiency: 0.98,
    champion_lift: 15.0, competitive_score: 51.8,
    is_at_risk: false, needs_battlecard: false,
    won_deals: 23, total_deals: 50,
  },
  {
    matchup_id: "m_008", our_product: "ProductY", competitor: "CompetitorD",
    segment: "mid-market", region: "NAMER",
    win_rate_category: "weak", competitive_risk: "high",
    trend_direction: "stable", competitive_action: "differentiate",
    win_rate: 28.0, win_rate_delta: 1.0,
    deal_size_advantage: 0.85, cycle_efficiency: 0.92,
    champion_lift: -5.0, competitive_score: 24.6,
    is_at_risk: true, needs_battlecard: true,
    won_deals: 14, total_deals: 50,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const category  = searchParams.get("category");
  const risk      = searchParams.get("risk");
  const product   = searchParams.get("product");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/competitive-win-rate`);
      if (category) url.searchParams.set("category", category);
      if (risk)     url.searchParams.set("risk", risk);
      if (product)  url.searchParams.set("product", product);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let matchups = [...mockMatchups];
  if (category) matchups = matchups.filter((m) => m.win_rate_category === category);
  if (risk)     matchups = matchups.filter((m) => m.competitive_risk === risk);
  if (product)  matchups = matchups.filter((m) => m.our_product === product);

  const category_counts: Record<string, number> = {};
  const risk_counts:     Record<string, number> = {};
  const trend_counts:    Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_wr = 0, total_score = 0, total_delta = 0,
      total_advantage = 0, total_cycle = 0;

  for (const m of mockMatchups) {
    category_counts[m.win_rate_category] = (category_counts[m.win_rate_category] || 0) + 1;
    risk_counts[m.competitive_risk]      = (risk_counts[m.competitive_risk] || 0) + 1;
    trend_counts[m.trend_direction]      = (trend_counts[m.trend_direction] || 0) + 1;
    action_counts[m.competitive_action]  = (action_counts[m.competitive_action] || 0) + 1;
    total_wr        += m.win_rate;
    total_score     += m.competitive_score;
    total_delta     += m.win_rate_delta;
    total_advantage += m.deal_size_advantage;
    total_cycle     += m.cycle_efficiency;
  }

  const n = mockMatchups.length;

  return NextResponse.json({
    matchups,
    summary: {
      total:                   n,
      category_counts,
      risk_counts,
      trend_counts,
      action_counts,
      avg_win_rate:            Math.round((total_wr / n) * 10) / 10,
      avg_competitive_score:   Math.round((total_score / n) * 10) / 10,
      avg_win_rate_delta:      Math.round((total_delta / n) * 10) / 10,
      at_risk_count:           mockMatchups.filter((m) => m.is_at_risk).length,
      battlecard_count:        mockMatchups.filter((m) => m.needs_battlecard).length,
      avg_deal_size_advantage: Math.round((total_advantage / n) * 100) / 100,
      avg_cycle_efficiency:    Math.round((total_cycle / n) * 100) / 100,
      dominant_count:          mockMatchups.filter((m) => m.win_rate_category === "dominant").length,
    },
  });
}
