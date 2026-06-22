import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[price-negotiation] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "d_001",
    account_id: "acc_001",
    rep_id: "rep_001",
    deal_name: "ERP Integration",
    account_name: "TechCorp SA",
    segment: "enterprise",
    list_price: 150000,
    proposed_price: 120000,
    discount_risk: "minimal",
    negotiation_stage: "counter_offer",
    pricing_strategy: "offer_value_add",
    margin_health: "strong",
    gross_margin_pct: 62.5,
    effective_discount_pct: 20.0,
    price_to_value_score: 74.2,
    negotiation_leverage: 82.0,
    walkaway_risk: 18.0,
    recommended_concession: 3750.0,
    is_margin_positive: true,
    is_strategic: true,
    days_to_close: 15,
    multi_year_deal: true,
    professional_services: 20000,
  },
  {
    deal_id: "d_002",
    account_id: "acc_002",
    rep_id: "rep_002",
    deal_name: "Platform Migration",
    account_name: "GlobalFinance SARL",
    segment: "enterprise",
    list_price: 320000,
    proposed_price: 220000,
    discount_risk: "critical",
    negotiation_stage: "stalled",
    pricing_strategy: "escalate_to_exec",
    margin_health: "critical",
    gross_margin_pct: 18.2,
    effective_discount_pct: 31.3,
    price_to_value_score: 28.5,
    negotiation_leverage: 22.0,
    walkaway_risk: 78.0,
    recommended_concession: 0.0,
    is_margin_positive: true,
    is_strategic: true,
    days_to_close: 5,
    multi_year_deal: false,
    professional_services: 0,
  },
  {
    deal_id: "d_003",
    account_id: "acc_003",
    rep_id: "rep_003",
    deal_name: "Analytics Suite",
    account_name: "MediaGroup SAS",
    segment: "mid_market",
    list_price: 85000,
    proposed_price: 72250,
    discount_risk: "minimal",
    negotiation_stage: "initial_offer",
    pricing_strategy: "hold_price",
    margin_health: "healthy",
    gross_margin_pct: 51.7,
    effective_discount_pct: 15.0,
    price_to_value_score: 66.8,
    negotiation_leverage: 74.0,
    walkaway_risk: 8.0,
    recommended_concession: 2125.0,
    is_margin_positive: true,
    is_strategic: false,
    days_to_close: 22,
    multi_year_deal: false,
    professional_services: 0,
  },
  {
    deal_id: "d_004",
    account_id: "acc_004",
    rep_id: "rep_001",
    deal_name: "Customer 360",
    account_name: "RetailChain Nord",
    segment: "mid_market",
    list_price: 95000,
    proposed_price: 66500,
    discount_risk: "high",
    negotiation_stage: "counter_offer",
    pricing_strategy: "escalate_to_exec",
    margin_health: "thin",
    gross_margin_pct: 32.3,
    effective_discount_pct: 30.0,
    price_to_value_score: 38.4,
    negotiation_leverage: 38.0,
    walkaway_risk: 52.0,
    recommended_concession: 0.0,
    is_margin_positive: true,
    is_strategic: false,
    days_to_close: 18,
    multi_year_deal: false,
    professional_services: 0,
  },
  {
    deal_id: "d_005",
    account_id: "acc_005",
    rep_id: "rep_004",
    deal_name: "Patient Data Platform",
    account_name: "HealthTech Pro",
    segment: "enterprise",
    list_price: 280000,
    proposed_price: 252000,
    discount_risk: "minimal",
    negotiation_stage: "final_terms",
    pricing_strategy: "offer_value_add",
    margin_health: "healthy",
    gross_margin_pct: 47.6,
    effective_discount_pct: 10.0,
    price_to_value_score: 81.3,
    negotiation_leverage: 88.0,
    walkaway_risk: 12.0,
    recommended_concession: 5600.0,
    is_margin_positive: true,
    is_strategic: true,
    days_to_close: 3,
    multi_year_deal: true,
    professional_services: 35000,
  },
  {
    deal_id: "d_006",
    account_id: "acc_006",
    rep_id: "rep_002",
    deal_name: "Supply Chain Intelligence",
    account_name: "LogisticsPlus SA",
    segment: "mid_market",
    list_price: 160000,
    proposed_price: 128000,
    discount_risk: "moderate",
    negotiation_stage: "counter_offer",
    pricing_strategy: "concede_strategic",
    margin_health: "healthy",
    gross_margin_pct: 53.1,
    effective_discount_pct: 20.0,
    price_to_value_score: 58.7,
    negotiation_leverage: 55.0,
    walkaway_risk: 42.0,
    recommended_concession: 4000.0,
    is_margin_positive: true,
    is_strategic: true,
    days_to_close: 25,
    multi_year_deal: false,
    professional_services: 15000,
  },
  {
    deal_id: "d_007",
    account_id: "acc_007",
    rep_id: "rep_003",
    deal_name: "LMS Platform",
    account_name: "EduSmart Group",
    segment: "smb",
    list_price: 52000,
    proposed_price: 48360,
    discount_risk: "minimal",
    negotiation_stage: "initial_offer",
    pricing_strategy: "hold_price",
    margin_health: "strong",
    gross_margin_pct: 68.4,
    effective_discount_pct: 7.0,
    price_to_value_score: 71.5,
    negotiation_leverage: 78.0,
    walkaway_risk: 5.0,
    recommended_concession: 936.0,
    is_margin_positive: true,
    is_strategic: false,
    days_to_close: 30,
    multi_year_deal: false,
    professional_services: 0,
  },
  {
    deal_id: "d_008",
    account_id: "acc_008",
    rep_id: "rep_004",
    deal_name: "Risk Analytics",
    account_name: "FinServ Capital",
    segment: "enterprise",
    list_price: 420000,
    proposed_price: 327600,
    discount_risk: "high",
    negotiation_stage: "counter_offer",
    pricing_strategy: "escalate_to_exec",
    margin_health: "thin",
    gross_margin_pct: 38.5,
    effective_discount_pct: 22.0,
    price_to_value_score: 52.1,
    negotiation_leverage: 45.0,
    walkaway_risk: 38.0,
    recommended_concession: 6300.0,
    is_margin_positive: true,
    is_strategic: true,
    days_to_close: 12,
    multi_year_deal: true,
    professional_services: 45000,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk     = searchParams.get("risk");
  const strategy = searchParams.get("strategy");
  const stage    = searchParams.get("stage");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/price-negotiation`);
      if (risk)     url.searchParams.set("risk", risk);
      if (strategy) url.searchParams.set("strategy", strategy);
      if (stage)    url.searchParams.set("stage", stage);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let deals = [...mockDeals];
  if (risk)     deals = deals.filter((d) => d.discount_risk === risk);
  if (strategy) deals = deals.filter((d) => d.pricing_strategy === strategy);
  if (stage)    deals = deals.filter((d) => d.negotiation_stage === stage);

  const risk_counts:     Record<string, number> = {};
  const strategy_counts: Record<string, number> = {};
  const stage_counts:    Record<string, number> = {};
  const margin_counts:   Record<string, number> = {};
  let total_margin = 0, total_disc = 0, total_lev = 0, total_walk = 0, total_ptv = 0;

  for (const d of mockDeals) {
    risk_counts[d.discount_risk]      = (risk_counts[d.discount_risk] || 0) + 1;
    strategy_counts[d.pricing_strategy] = (strategy_counts[d.pricing_strategy] || 0) + 1;
    stage_counts[d.negotiation_stage] = (stage_counts[d.negotiation_stage] || 0) + 1;
    margin_counts[d.margin_health]    = (margin_counts[d.margin_health] || 0) + 1;
    total_margin += d.gross_margin_pct;
    total_disc   += d.effective_discount_pct;
    total_lev    += d.negotiation_leverage;
    total_walk   += d.walkaway_risk;
    total_ptv    += d.price_to_value_score;
  }

  const n = mockDeals.length;

  return sealResponse(NextResponse.json({
    deals,
    summary: {
      total:                      n,
      risk_counts,
      stage_counts,
      strategy_counts,
      margin_health_counts:       margin_counts,
      avg_gross_margin_pct:       Math.round((total_margin / n) * 10) / 10,
      avg_effective_discount:     Math.round((total_disc / n) * 10) / 10,
      avg_negotiation_leverage:   Math.round((total_lev / n) * 10) / 10,
      avg_walkaway_risk:          Math.round((total_walk / n) * 10) / 10,
      high_risk_count:            mockDeals.filter((d) => ["high", "critical"].includes(d.discount_risk)).length,
      strategic_count:            mockDeals.filter((d) => d.is_strategic).length,
      walk_away_count:            mockDeals.filter((d) => d.pricing_strategy === "walk_away").length,
      avg_price_to_value_score:   Math.round((total_ptv / n) * 10) / 10,
    },
  }));
}
