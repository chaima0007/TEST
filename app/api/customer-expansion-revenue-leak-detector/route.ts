import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockAccounts = [
  {
    account_id: "acc_001", region: "West",
    expansion_leak_risk: "low", leak_pattern: "none",
    leak_severity: "captured", recommended_action: "no_action",
    upsell_neglect_score: 0.0, cross_sell_gap_score: 0.0,
    renewal_pricing_score: 0.0, champion_leverage_score: 0.0,
    expansion_leak_composite: 0.0, is_revenue_leaking: false, requires_immediate_action: false,
    estimated_leaked_revenue_usd: 0.0,
    leak_signal: "Expansion motion healthy — all revenue opportunities being actively pursued",
  },
  {
    account_id: "acc_002", region: "East",
    expansion_leak_risk: "low", leak_pattern: "upsell_neglect",
    leak_severity: "watch", recommended_action: "expansion_outreach",
    upsell_neglect_score: 15.0, cross_sell_gap_score: 8.0,
    renewal_pricing_score: 6.0, champion_leverage_score: 5.0,
    expansion_leak_composite: 9.5, is_revenue_leaking: false, requires_immediate_action: false,
    estimated_leaked_revenue_usd: 4750.0,
    leak_signal: "Upsell neglect — 35d since expansion discussion — composite 10",
  },
  {
    account_id: "acc_003", region: "Central",
    expansion_leak_risk: "moderate", leak_pattern: "cross_sell_gap",
    leak_severity: "watch", recommended_action: "expansion_outreach",
    upsell_neglect_score: 20.0, cross_sell_gap_score: 30.0,
    renewal_pricing_score: 12.0, champion_leverage_score: 10.0,
    expansion_leak_composite: 19.8, is_revenue_leaking: false, requires_immediate_action: false,
    estimated_leaked_revenue_usd: 19800.0,
    leak_signal: "Cross sell gap — 20% cross-sell adoption — 60d since expansion discussion — composite 20",
  },
  {
    account_id: "acc_004", region: "Northeast",
    expansion_leak_risk: "moderate", leak_pattern: "renewal_underpricing",
    leak_severity: "watch", recommended_action: "expansion_outreach",
    upsell_neglect_score: 15.0, cross_sell_gap_score: 18.0,
    renewal_pricing_score: 28.0, champion_leverage_score: 15.0,
    expansion_leak_composite: 19.5, is_revenue_leaking: false, requires_immediate_action: false,
    estimated_leaked_revenue_usd: 29250.0,
    leak_signal: "Renewal underpricing — 12pp below benchmark — NPS 78 with no price increase — composite 20",
  },
  {
    account_id: "acc_005", region: "Southeast",
    expansion_leak_risk: "high", leak_pattern: "champion_not_leveraged",
    leak_severity: "leaking", recommended_action: "expansion_outreach",
    upsell_neglect_score: 35.0, cross_sell_gap_score: 30.0,
    renewal_pricing_score: 20.0, champion_leverage_score: 40.0,
    expansion_leak_composite: 31.0, is_revenue_leaking: false, requires_immediate_action: true,
    estimated_leaked_revenue_usd: 62000.0,
    leak_signal: "Champion not leveraged — no QBR in 180d — 0 stakeholder intros — 75d since expansion discussion — composite 31",
  },
  {
    account_id: "acc_006", region: "West",
    expansion_leak_risk: "high", leak_pattern: "expansion_stall",
    leak_severity: "leaking", recommended_action: "qbr_scheduling",
    upsell_neglect_score: 45.0, cross_sell_gap_score: 42.0,
    renewal_pricing_score: 28.0, champion_leverage_score: 25.0,
    expansion_leak_composite: 37.3, is_revenue_leaking: false, requires_immediate_action: true,
    estimated_leaked_revenue_usd: 111900.0,
    leak_signal: "Expansion stall — 3 aged opps 90d+ — 15% cross-sell adoption — 92d since expansion discussion — composite 37",
  },
  {
    account_id: "acc_007", region: "APAC",
    expansion_leak_risk: "critical", leak_pattern: "expansion_stall",
    leak_severity: "critical", recommended_action: "qbr_scheduling",
    upsell_neglect_score: 70.0, cross_sell_gap_score: 65.0,
    renewal_pricing_score: 50.0, champion_leverage_score: 55.0,
    expansion_leak_composite: 61.5, is_revenue_leaking: true, requires_immediate_action: true,
    estimated_leaked_revenue_usd: 246000.0,
    leak_signal: "Expansion stall — 95% utilization with no upsell attempt — 5 aged opps 90d+ — no QBR in 180d — composite 62",
  },
  {
    account_id: "acc_008", region: "EMEA",
    expansion_leak_risk: "critical", leak_pattern: "champion_not_leveraged",
    leak_severity: "critical", recommended_action: "executive_alignment",
    upsell_neglect_score: 75.0, cross_sell_gap_score: 70.0,
    renewal_pricing_score: 60.0, champion_leverage_score: 65.0,
    expansion_leak_composite: 68.3, is_revenue_leaking: true, requires_immediate_action: true,
    estimated_leaked_revenue_usd: 341500.0,
    leak_signal: "Champion not leveraged — 0 stakeholder intros — no QBR in 180d — 10% cross-sell adoption — 120d since expansion discussion — composite 68",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/customer-expansion-revenue-leak-detector`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let accounts = [...mockAccounts];
  if (risk)    accounts = accounts.filter((a) => a.expansion_leak_risk === risk);
  if (pattern) accounts = accounts.filter((a) => a.leak_pattern         === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_u = 0, total_c = 0, total_r = 0, total_h = 0, total_rev = 0;

  for (const a of mockAccounts) {
    risk_counts[a.expansion_leak_risk]   = (risk_counts[a.expansion_leak_risk] || 0) + 1;
    pattern_counts[a.leak_pattern]       = (pattern_counts[a.leak_pattern] || 0) + 1;
    severity_counts[a.leak_severity]     = (severity_counts[a.leak_severity] || 0) + 1;
    action_counts[a.recommended_action]  = (action_counts[a.recommended_action] || 0) + 1;
    total_comp += a.expansion_leak_composite;
    total_u    += a.upsell_neglect_score;
    total_c    += a.cross_sell_gap_score;
    total_r    += a.renewal_pricing_score;
    total_h    += a.champion_leverage_score;
    total_rev  += a.estimated_leaked_revenue_usd;
  }

  const n = mockAccounts.length;

  return NextResponse.json({
    accounts,
    summary: {
      total:                                n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_expansion_leak_composite:         Math.round((total_comp / n) * 10) / 10,
      leaking_count:                        mockAccounts.filter((a) => a.is_revenue_leaking).length,
      immediate_action_count:               mockAccounts.filter((a) => a.requires_immediate_action).length,
      avg_upsell_neglect_score:             Math.round((total_u / n) * 10) / 10,
      avg_cross_sell_gap_score:             Math.round((total_c / n) * 10) / 10,
      avg_renewal_pricing_score:            Math.round((total_r / n) * 10) / 10,
      avg_champion_leverage_score:          Math.round((total_h / n) * 10) / 10,
      total_estimated_leaked_revenue_usd:   Math.round(total_rev * 100) / 100,
    },
  });
}
