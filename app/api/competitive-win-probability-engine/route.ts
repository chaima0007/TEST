import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "deal_001", deal_name: "TechCorp ELA vs Salesforce", rep_id: "rep_001",
    competitor_name: "Salesforce",
    win_probability_tier: "very_likely", win_risk: "low",
    primary_win_factor: "champion", recommended_action: "maintain_course",
    champion_score: 95.0, competitive_position_score: 75.2, relationship_momentum_score: 82.3,
    deal_strength_score: 65.0, win_probability_pct: 83.9,
    is_at_risk: false, requires_executive_intervention: false,
    estimated_win_value_usd: 419500.0,
    win_signal: "POC won vs Salesforce — champion strong, path to close clear",
    deal_value_usd: 500000.0,
  },
  {
    deal_id: "deal_002", deal_name: "Meridian Finance vs Oracle", rep_id: "rep_002",
    competitor_name: "Oracle",
    win_probability_tier: "very_unlikely", win_risk: "critical",
    primary_win_factor: "features", recommended_action: "executive_alignment",
    champion_score: 18.0, competitive_position_score: 22.0, relationship_momentum_score: 15.0,
    deal_strength_score: 42.0, win_probability_pct: 21.2,
    is_at_risk: true, requires_executive_intervention: true,
    estimated_win_value_usd: 190800.0,
    win_signal: "at risk of losing to Oracle — immediate intervention required",
    deal_value_usd: 900000.0,
  },
  {
    deal_id: "deal_003", deal_name: "Apex Cloud vs HubSpot", rep_id: "rep_003",
    competitor_name: "HubSpot",
    win_probability_tier: "likely", win_risk: "low",
    primary_win_factor: "champion", recommended_action: "maintain_course",
    champion_score: 85.0, competitive_position_score: 68.5, relationship_momentum_score: 70.2,
    deal_strength_score: 55.0, win_probability_pct: 74.0,
    is_at_risk: false, requires_executive_intervention: false,
    estimated_win_value_usd: 207200.0,
    win_signal: "strong position vs HubSpot — 74% win probability, maintain course",
    deal_value_usd: 280000.0,
  },
  {
    deal_id: "deal_004", deal_name: "Orion Healthcare vs Microsoft", rep_id: "rep_001",
    competitor_name: "Microsoft",
    win_probability_tier: "toss_up", win_risk: "high",
    primary_win_factor: "features", recommended_action: "feature_demo",
    champion_score: 55.0, competitive_position_score: 44.0, relationship_momentum_score: 48.0,
    deal_strength_score: 50.0, win_probability_pct: 49.1,
    is_at_risk: true, requires_executive_intervention: true,
    estimated_win_value_usd: 220950.0,
    win_signal: "competitive with Microsoft at 49% win probability",
    deal_value_usd: 450000.0,
  },
  {
    deal_id: "deal_005", deal_name: "Lumina Retail vs SAP", rep_id: "rep_002",
    competitor_name: "SAP",
    win_probability_tier: "likely", win_risk: "moderate",
    primary_win_factor: "momentum", recommended_action: "maintain_course",
    champion_score: 72.0, competitive_position_score: 58.0, relationship_momentum_score: 75.0,
    deal_strength_score: 60.0, win_probability_pct: 66.4,
    is_at_risk: false, requires_executive_intervention: false,
    estimated_win_value_usd: 99600.0,
    win_signal: "strong position vs SAP — 66% win probability, maintain course",
    deal_value_usd: 150000.0,
  },
  {
    deal_id: "deal_006", deal_name: "Cascade Logistics vs Veeva", rep_id: "rep_004",
    competitor_name: "Veeva",
    win_probability_tier: "unlikely", win_risk: "high",
    primary_win_factor: "price", recommended_action: "price_adjustment",
    champion_score: 38.0, competitive_position_score: 32.0, relationship_momentum_score: 40.0,
    deal_strength_score: 48.0, win_probability_pct: 37.5,
    is_at_risk: true, requires_executive_intervention: false,
    estimated_win_value_usd: 112500.0,
    win_signal: "displacing incumbent Veeva — win rate historically 28%",
    deal_value_usd: 300000.0,
  },
  {
    deal_id: "deal_007", deal_name: "Nexus Energy vs Tableau", rep_id: "rep_003",
    competitor_name: "Tableau",
    win_probability_tier: "very_likely", win_risk: "low",
    primary_win_factor: "champion", recommended_action: "maintain_course",
    champion_score: 92.0, competitive_position_score: 82.0, relationship_momentum_score: 78.0,
    deal_strength_score: 62.0, win_probability_pct: 82.8,
    is_at_risk: false, requires_executive_intervention: false,
    estimated_win_value_usd: 182160.0,
    win_signal: "executive + economic buyer aligned — Tableau at disadvantage",
    deal_value_usd: 220000.0,
  },
  {
    deal_id: "deal_008", deal_name: "Vertex Pharma vs Workday", rep_id: "rep_001",
    competitor_name: "Workday",
    win_probability_tier: "toss_up", win_risk: "moderate",
    primary_win_factor: "features", recommended_action: "strengthen_champion",
    champion_score: 50.0, competitive_position_score: 55.0, relationship_momentum_score: 52.0,
    deal_strength_score: 55.0, win_probability_pct: 52.8,
    is_at_risk: false, requires_executive_intervention: false,
    estimated_win_value_usd: 343200.0,
    win_signal: "competitive with Workday at 53% win probability",
    deal_value_usd: 650000.0,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const tier = searchParams.get("tier");
  const risk = searchParams.get("risk");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/competitive-win-probability-engine`);
      if (tier) url.searchParams.set("tier", tier);
      if (risk) url.searchParams.set("risk", risk);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let deals = [...mockDeals];
  if (tier) deals = deals.filter((d) => d.win_probability_tier === tier);
  if (risk) deals = deals.filter((d) => d.win_risk === risk);

  const tier_counts:   Record<string, number> = {};
  const risk_counts:   Record<string, number> = {};
  const factor_counts: Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  let total_pct = 0, total_ch = 0, total_cp = 0, total_rm = 0, total_ds = 0, total_wpipe = 0;

  for (const d of mockDeals) {
    tier_counts[d.win_probability_tier]  = (tier_counts[d.win_probability_tier] || 0) + 1;
    risk_counts[d.win_risk]              = (risk_counts[d.win_risk] || 0) + 1;
    factor_counts[d.primary_win_factor]  = (factor_counts[d.primary_win_factor] || 0) + 1;
    action_counts[d.recommended_action]  = (action_counts[d.recommended_action] || 0) + 1;
    total_pct   += d.win_probability_pct;
    total_ch    += d.champion_score;
    total_cp    += d.competitive_position_score;
    total_rm    += d.relationship_momentum_score;
    total_ds    += d.deal_strength_score;
    total_wpipe += d.estimated_win_value_usd;
  }

  const n = mockDeals.length;

  return NextResponse.json({
    deals,
    summary: {
      total: n,
      tier_counts,
      risk_counts,
      factor_counts,
      action_counts,
      avg_win_probability_pct:          Math.round((total_pct / n) * 10) / 10,
      at_risk_count:                    mockDeals.filter((d) => d.is_at_risk).length,
      executive_intervention_count:     mockDeals.filter((d) => d.requires_executive_intervention).length,
      avg_champion_score:               Math.round((total_ch / n) * 10) / 10,
      avg_competitive_position_score:   Math.round((total_cp / n) * 10) / 10,
      avg_relationship_momentum_score:  Math.round((total_rm / n) * 10) / 10,
      avg_deal_strength_score:          Math.round((total_ds / n) * 10) / 10,
      total_weighted_pipeline_usd:      Math.round(total_wpipe),
    },
  });
}
