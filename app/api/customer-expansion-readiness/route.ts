import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockAccounts = [
  {
    account_id: "acc_001", account_name: "Apex Technologies", industry: "Technology", region: "NAMER",
    expansion_readiness_tier: "primed", expansion_motion: "seat_expansion",
    expansion_priority: "urgent", expansion_action: "close_expansion",
    product_depth_score: 83.2, relationship_strength_score: 78.4,
    financial_health_score: 74.6, timing_score: 88.0,
    expansion_readiness_score: 80.9, estimated_expansion_arr: 346576,
    expansion_confidence_score: 100.0, is_expansion_ready: true, needs_success_intervention: false,
    current_mrr: 42000, contract_end_months: 6,
    seats_used: 180, seats_purchased: 200, max_seats_available: 500,
    feature_adoption_rate: 72.0, nps_score: 48.0, avg_mau_pct: 88.0,
  },
  {
    account_id: "acc_002", account_name: "GlobalFinance Corp", industry: "Financial Services", region: "EMEA",
    expansion_readiness_tier: "ready", expansion_motion: "cross_sell",
    expansion_priority: "high", expansion_action: "engage",
    product_depth_score: 62.4, relationship_strength_score: 68.2,
    financial_health_score: 58.8, timing_score: 54.0,
    expansion_readiness_score: 63.1, estimated_expansion_arr: 187200,
    expansion_confidence_score: 80.0, is_expansion_ready: true, needs_success_intervention: false,
    current_mrr: 28000, contract_end_months: 9,
    seats_used: 85, seats_purchased: 100, max_seats_available: 200,
    feature_adoption_rate: 58.0, nps_score: 32.0, avg_mau_pct: 72.0,
  },
  {
    account_id: "acc_003", account_name: "RetailPlex", industry: "Retail", region: "APAC",
    expansion_readiness_tier: "not_ready", expansion_motion: "hold",
    expansion_priority: "low", expansion_action: "nurture",
    product_depth_score: 28.4, relationship_strength_score: 32.6,
    financial_health_score: 24.2, timing_score: 18.0,
    expansion_readiness_score: 27.4, estimated_expansion_arr: 0,
    expansion_confidence_score: 20.0, is_expansion_ready: false, needs_success_intervention: true,
    current_mrr: 8400, contract_end_months: 14,
    seats_used: 22, seats_purchased: 50, max_seats_available: 100,
    feature_adoption_rate: 24.0, nps_score: -18.0, avg_mau_pct: 34.0,
  },
  {
    account_id: "acc_004", account_name: "MedCore Systems", industry: "Healthcare", region: "NAMER",
    expansion_readiness_tier: "primed", expansion_motion: "upsell_tier",
    expansion_priority: "urgent", expansion_action: "close_expansion",
    product_depth_score: 88.6, relationship_strength_score: 84.2,
    financial_health_score: 82.4, timing_score: 76.0,
    expansion_readiness_score: 84.2, estimated_expansion_arr: 524400,
    expansion_confidence_score: 100.0, is_expansion_ready: true, needs_success_intervention: false,
    current_mrr: 68000, contract_end_months: 5,
    seats_used: 340, seats_purchased: 350, max_seats_available: 500,
    feature_adoption_rate: 88.0, nps_score: 72.0, avg_mau_pct: 94.0,
  },
  {
    account_id: "acc_005", account_name: "Logistics Hub", industry: "Logistics", region: "LATAM",
    expansion_readiness_tier: "building", expansion_motion: "upsell_tier",
    expansion_priority: "medium", expansion_action: "nurture",
    product_depth_score: 44.8, relationship_strength_score: 48.2,
    financial_health_score: 38.6, timing_score: 32.0,
    expansion_readiness_score: 42.8, estimated_expansion_arr: 48600,
    expansion_confidence_score: 60.0, is_expansion_ready: false, needs_success_intervention: false,
    current_mrr: 12000, contract_end_months: 11,
    seats_used: 48, seats_purchased: 60, max_seats_available: 150,
    feature_adoption_rate: 44.0, nps_score: 18.0, avg_mau_pct: 62.0,
  },
  {
    account_id: "acc_006", account_name: "EduTech Solutions", industry: "Education", region: "EMEA",
    expansion_readiness_tier: "ready", expansion_motion: "renewal_lock",
    expansion_priority: "high", expansion_action: "engage",
    product_depth_score: 66.4, relationship_strength_score: 72.6,
    financial_health_score: 54.2, timing_score: 72.0,
    expansion_readiness_score: 66.8, estimated_expansion_arr: 112800,
    expansion_confidence_score: 80.0, is_expansion_ready: true, needs_success_intervention: false,
    current_mrr: 18000, contract_end_months: 3,
    seats_used: 140, seats_purchased: 150, max_seats_available: 300,
    feature_adoption_rate: 62.0, nps_score: 54.0, avg_mau_pct: 78.0,
  },
  {
    account_id: "acc_007", account_name: "ManufacturePro", industry: "Manufacturing", region: "EMEA",
    expansion_readiness_tier: "not_ready", expansion_motion: "hold",
    expansion_priority: "low", expansion_action: "maintain",
    product_depth_score: 32.6, relationship_strength_score: 28.4,
    financial_health_score: 18.8, timing_score: 8.0,
    expansion_readiness_score: 24.6, estimated_expansion_arr: 0,
    expansion_confidence_score: 0.0, is_expansion_ready: false, needs_success_intervention: true,
    current_mrr: 6200, contract_end_months: 18,
    seats_used: 18, seats_purchased: 30, max_seats_available: 60,
    feature_adoption_rate: 28.0, nps_score: -32.0, avg_mau_pct: 28.0,
  },
  {
    account_id: "acc_008", account_name: "CloudWave Consulting", industry: "Professional Services", region: "NAMER",
    expansion_readiness_tier: "ready", expansion_motion: "cross_sell",
    expansion_priority: "high", expansion_action: "engage",
    product_depth_score: 72.8, relationship_strength_score: 66.4,
    financial_health_score: 64.6, timing_score: 62.0,
    expansion_readiness_score: 68.0, estimated_expansion_arr: 226800,
    expansion_confidence_score: 80.0, is_expansion_ready: true, needs_success_intervention: false,
    current_mrr: 34000, contract_end_months: 8,
    seats_used: 92, seats_purchased: 100, max_seats_available: 250,
    feature_adoption_rate: 68.0, nps_score: 42.0, avg_mau_pct: 82.0,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const tier     = searchParams.get("tier");
  const motion   = searchParams.get("motion");
  const region   = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/customer-expansion-readiness`);
      if (tier)   url.searchParams.set("tier", tier);
      if (motion) url.searchParams.set("motion", motion);
      if (region) url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let accounts = [...mockAccounts];
  if (tier)   accounts = accounts.filter((a) => a.expansion_readiness_tier === tier);
  if (motion) accounts = accounts.filter((a) => a.expansion_motion === motion);
  if (region) accounts = accounts.filter((a) => a.region === region);

  const tier_counts:     Record<string, number> = {};
  const motion_counts:   Record<string, number> = {};
  const priority_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_readiness = 0, total_prod = 0, total_rel = 0,
      total_timing = 0, total_conf = 0, total_arr = 0;

  for (const a of mockAccounts) {
    tier_counts[a.expansion_readiness_tier]   = (tier_counts[a.expansion_readiness_tier] || 0) + 1;
    motion_counts[a.expansion_motion]         = (motion_counts[a.expansion_motion] || 0) + 1;
    priority_counts[a.expansion_priority]     = (priority_counts[a.expansion_priority] || 0) + 1;
    action_counts[a.expansion_action]         = (action_counts[a.expansion_action] || 0) + 1;
    total_readiness += a.expansion_readiness_score;
    total_prod      += a.product_depth_score;
    total_rel       += a.relationship_strength_score;
    total_timing    += a.timing_score;
    total_conf      += a.expansion_confidence_score;
    total_arr       += a.estimated_expansion_arr;
  }

  const n = mockAccounts.length;

  return NextResponse.json({
    accounts,
    summary: {
      total: n,
      tier_counts,
      motion_counts,
      priority_counts,
      action_counts,
      avg_expansion_readiness_score:   Math.round((total_readiness / n) * 10) / 10,
      total_estimated_expansion_arr:   Math.round(total_arr),
      ready_count:                     mockAccounts.filter((a) => a.is_expansion_ready).length,
      intervention_needed_count:       mockAccounts.filter((a) => a.needs_success_intervention).length,
      avg_product_depth_score:         Math.round((total_prod / n) * 10) / 10,
      avg_relationship_strength_score: Math.round((total_rel / n) * 10) / 10,
      avg_timing_score:                Math.round((total_timing / n) * 10) / 10,
      avg_expansion_confidence_score:  Math.round((total_conf / n) * 10) / 10,
    },
  });
}
