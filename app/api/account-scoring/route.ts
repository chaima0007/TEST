import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[account-scoring] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockAccounts = [
  {
    account_id: "acc_001", account_name: "Acme Corp",
    industry: "SaaS", region: "NAMER",
    account_tier: "enterprise", account_health: "excellent",
    engagement_level: "high", account_action: "expand",
    health_score: 82.4, engagement_score: 76.5,
    growth_score: 71.2, fit_score: 78.3,
    churn_risk: 14.2, expansion_probability: 78.9,
    composite_score: 78.1,
    is_at_risk: false, needs_attention: false,
    total_mrr: 28000, expansion_mrr: 4200,
    seats_used: 22, seats_total: 30, upsell_opportunities: 4,
  },
  {
    account_id: "acc_002", account_name: "Globex Industries",
    industry: "Manufacturing", region: "EMEA",
    account_tier: "strategic", account_health: "excellent",
    engagement_level: "high", account_action: "retain",
    health_score: 88.7, engagement_score: 82.3,
    growth_score: 54.0, fit_score: 90.1,
    churn_risk: 8.5, expansion_probability: 58.6,
    composite_score: 80.2,
    is_at_risk: false, needs_attention: false,
    total_mrr: 65000, expansion_mrr: 2000,
    seats_used: 48, seats_total: 50, upsell_opportunities: 2,
  },
  {
    account_id: "acc_003", account_name: "TechStart LLC",
    industry: "Fintech", region: "APAC",
    account_tier: "smb", account_health: "fair",
    engagement_level: "medium", account_action: "nurture",
    health_score: 52.1, engagement_score: 48.7,
    growth_score: 62.4, fit_score: 41.8,
    churn_risk: 34.8, expansion_probability: 56.2,
    composite_score: 51.8,
    is_at_risk: false, needs_attention: false,
    total_mrr: 3200, expansion_mrr: 800,
    seats_used: 8, seats_total: 15, upsell_opportunities: 3,
  },
  {
    account_id: "acc_004", account_name: "MegaCorp Solutions",
    industry: "Consulting", region: "NAMER",
    account_tier: "strategic", account_health: "at_risk",
    engagement_level: "low", account_action: "rescue",
    health_score: 31.6, engagement_score: 28.4,
    growth_score: 18.5, fit_score: 72.4,
    churn_risk: 68.2, expansion_probability: 22.8,
    composite_score: 36.4,
    is_at_risk: true, needs_attention: true,
    total_mrr: 82000, expansion_mrr: 0,
    seats_used: 35, seats_total: 80, upsell_opportunities: 0,
  },
  {
    account_id: "acc_005", account_name: "VentureHub Inc",
    industry: "Startup", region: "LATAM",
    account_tier: "growth", account_health: "good",
    engagement_level: "medium", account_action: "expand",
    health_score: 66.3, engagement_score: 59.8,
    growth_score: 75.6, fit_score: 58.2,
    churn_risk: 28.4, expansion_probability: 68.4,
    composite_score: 65.9,
    is_at_risk: false, needs_attention: false,
    total_mrr: 9500, expansion_mrr: 1800,
    seats_used: 12, seats_total: 20, upsell_opportunities: 5,
  },
  {
    account_id: "acc_006", account_name: "DataSystems GmbH",
    industry: "Enterprise Software", region: "EMEA",
    account_tier: "enterprise", account_health: "churning",
    engagement_level: "dormant", account_action: "rescue",
    health_score: 18.2, engagement_score: 12.6,
    growth_score: 8.4, fit_score: 55.7,
    churn_risk: 84.5, expansion_probability: 9.2,
    composite_score: 22.1,
    is_at_risk: true, needs_attention: true,
    total_mrr: 34000, expansion_mrr: 0,
    seats_used: 10, seats_total: 40, upsell_opportunities: 0,
  },
  {
    account_id: "acc_007", account_name: "CloudPeak Analytics",
    industry: "Analytics", region: "APAC",
    account_tier: "growth", account_health: "excellent",
    engagement_level: "high", account_action: "expand",
    health_score: 79.4, engagement_score: 74.2,
    growth_score: 80.3, fit_score: 64.6,
    churn_risk: 16.8, expansion_probability: 77.3,
    composite_score: 74.8,
    is_at_risk: false, needs_attention: false,
    total_mrr: 12000, expansion_mrr: 3500,
    seats_used: 14, seats_total: 25, upsell_opportunities: 4,
  },
  {
    account_id: "acc_008", account_name: "RetailEdge Corp",
    industry: "Retail", region: "NAMER",
    account_tier: "smb", account_health: "fair",
    engagement_level: "low", account_action: "monitor",
    health_score: 44.8, engagement_score: 32.1,
    growth_score: 35.2, fit_score: 38.4,
    churn_risk: 42.6, expansion_probability: 34.1,
    composite_score: 38.7,
    is_at_risk: false, needs_attention: true,
    total_mrr: 2400, expansion_mrr: 200,
    seats_used: 5, seats_total: 10, upsell_opportunities: 1,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const tier   = searchParams.get("tier");
  const health = searchParams.get("health");
  const region = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/account-scoring`);
      if (tier)   url.searchParams.set("tier", tier);
      if (health) url.searchParams.set("health", health);
      if (region) url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let accounts = [...mockAccounts];
  if (tier)   accounts = accounts.filter((a) => a.account_tier === tier);
  if (health) accounts = accounts.filter((a) => a.account_health === health);
  if (region) accounts = accounts.filter((a) => a.region === region);

  const tier_counts:       Record<string, number> = {};
  const health_counts:     Record<string, number> = {};
  const engagement_counts: Record<string, number> = {};
  const action_counts:     Record<string, number> = {};
  let total_health = 0, total_comp = 0, total_churn = 0,
      total_expand = 0, total_growth = 0;

  for (const a of mockAccounts) {
    tier_counts[a.account_tier]       = (tier_counts[a.account_tier] || 0) + 1;
    health_counts[a.account_health]   = (health_counts[a.account_health] || 0) + 1;
    engagement_counts[a.engagement_level] = (engagement_counts[a.engagement_level] || 0) + 1;
    action_counts[a.account_action]   = (action_counts[a.account_action] || 0) + 1;
    total_health  += a.health_score;
    total_comp    += a.composite_score;
    total_churn   += a.churn_risk;
    total_expand  += a.expansion_probability;
    total_growth  += a.growth_score;
  }

  const n = mockAccounts.length;

  return sealResponse(NextResponse.json({
    accounts,
    summary: {
      total:                     n,
      tier_counts,
      health_counts,
      engagement_counts,
      action_counts,
      avg_health_score:          Math.round((total_health / n) * 10) / 10,
      avg_composite_score:       Math.round((total_comp / n) * 10) / 10,
      at_risk_count:             mockAccounts.filter((a) => a.is_at_risk).length,
      needs_attention_count:     mockAccounts.filter((a) => a.needs_attention).length,
      avg_churn_risk:            Math.round((total_churn / n) * 10) / 10,
      avg_expansion_probability: Math.round((total_expand / n) * 10) / 10,
      high_value_count:          mockAccounts.filter((a) => ["strategic", "enterprise"].includes(a.account_tier)).length,
      avg_growth_score:          Math.round((total_growth / n) * 10) / 10,
    },
  }));
}
