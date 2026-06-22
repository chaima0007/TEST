import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[account-expansion] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockAccounts = [
  {
    account_id: "a_001",
    account_name: "TechCorp SA",
    csm_id: "csm_001",
    segment: "enterprise",
    current_arr: 250000,
    contract_end_days: 120,
    expansion_type: "upsell",
    expansion_readiness: "ready_now",
    churn_signal: "none",
    expansion_action: "pitch_now",
    expansion_score: 82.4,
    health_score: 78.5,
    churn_risk_score: 8.0,
    adoption_rate: 75.0,
    feature_utilization: 60.0,
    expansion_potential: 66360.0,
    nrr_forecast: 128.4,
    is_at_risk: false,
    is_ready_to_expand: true,
    active_users: 45,
    licensed_users: 60,
    nps_score: 52,
    whitespace_products: 4,
    growth_since_start_pct: 25,
  },
  {
    account_id: "a_002",
    account_name: "GlobalFinance SARL",
    csm_id: "csm_002",
    segment: "enterprise",
    current_arr: 420000,
    contract_end_days: 35,
    expansion_type: "renewal_plus",
    expansion_readiness: "not_ready",
    churn_signal: "high",
    expansion_action: "risk_intervention",
    expansion_score: 18.5,
    health_score: 32.0,
    churn_risk_score: 72.0,
    adoption_rate: 35.0,
    feature_utilization: 25.0,
    expansion_potential: 9282.0,
    nrr_forecast: 71.2,
    is_at_risk: true,
    is_ready_to_expand: false,
    active_users: 21,
    licensed_users: 60,
    nps_score: -28,
    whitespace_products: 2,
    growth_since_start_pct: -5,
  },
  {
    account_id: "a_003",
    account_name: "MediaGroup SAS",
    csm_id: "csm_001",
    segment: "mid_market",
    current_arr: 85000,
    contract_end_days: 75,
    expansion_type: "cross_sell",
    expansion_readiness: "upcoming",
    churn_signal: "low",
    expansion_action: "schedule_qbr",
    expansion_score: 61.8,
    health_score: 68.5,
    churn_risk_score: 18.0,
    adoption_rate: 70.0,
    feature_utilization: 55.0,
    expansion_potential: 17765.0,
    nrr_forecast: 112.3,
    is_at_risk: false,
    is_ready_to_expand: false,
    active_users: 28,
    licensed_users: 40,
    nps_score: 35,
    whitespace_products: 3,
    growth_since_start_pct: 15,
  },
  {
    account_id: "a_004",
    account_name: "HealthTech Pro",
    csm_id: "csm_003",
    segment: "enterprise",
    current_arr: 380000,
    contract_end_days: 180,
    expansion_type: "platform_add",
    expansion_readiness: "ready_now",
    churn_signal: "none",
    expansion_action: "pitch_now",
    expansion_score: 88.7,
    health_score: 91.2,
    churn_risk_score: 5.0,
    adoption_rate: 88.0,
    feature_utilization: 70.0,
    expansion_potential: 101080.0,
    nrr_forecast: 141.6,
    is_at_risk: false,
    is_ready_to_expand: true,
    active_users: 88,
    licensed_users: 100,
    nps_score: 68,
    whitespace_products: 5,
    growth_since_start_pct: 40,
  },
  {
    account_id: "a_005",
    account_name: "RetailChain Nord",
    csm_id: "csm_002",
    segment: "mid_market",
    current_arr: 120000,
    contract_end_days: 20,
    expansion_type: "renewal_plus",
    expansion_readiness: "not_ready",
    churn_signal: "critical",
    expansion_action: "risk_intervention",
    expansion_score: 12.0,
    health_score: 25.0,
    churn_risk_score: 88.0,
    adoption_rate: 22.0,
    feature_utilization: 18.0,
    expansion_potential: 3384.0,
    nrr_forecast: 56.4,
    is_at_risk: true,
    is_ready_to_expand: false,
    active_users: 11,
    licensed_users: 50,
    nps_score: -55,
    whitespace_products: 1,
    growth_since_start_pct: -15,
  },
  {
    account_id: "a_006",
    account_name: "LogisticsPlus SA",
    csm_id: "csm_003",
    segment: "mid_market",
    current_arr: 95000,
    contract_end_days: 95,
    expansion_type: "upsell",
    expansion_readiness: "needs_nurturing",
    churn_signal: "medium",
    expansion_action: "nurture_adoption",
    expansion_score: 42.3,
    health_score: 51.8,
    churn_risk_score: 35.0,
    adoption_rate: 52.0,
    feature_utilization: 40.0,
    expansion_potential: 11527.0,
    nrr_forecast: 99.7,
    is_at_risk: false,
    is_ready_to_expand: false,
    active_users: 26,
    licensed_users: 50,
    nps_score: 12,
    whitespace_products: 2,
    growth_since_start_pct: 5,
  },
  {
    account_id: "a_007",
    account_name: "EduSmart Group",
    csm_id: "csm_001",
    segment: "smb",
    current_arr: 48000,
    contract_end_days: 150,
    expansion_type: "new_division",
    expansion_readiness: "ready_now",
    churn_signal: "none",
    expansion_action: "pitch_now",
    expansion_score: 74.5,
    health_score: 82.0,
    churn_risk_score: 6.0,
    adoption_rate: 90.0,
    feature_utilization: 65.0,
    expansion_potential: 14256.0,
    nrr_forecast: 124.8,
    is_at_risk: false,
    is_ready_to_expand: true,
    active_users: 27,
    licensed_users: 30,
    nps_score: 58,
    whitespace_products: 3,
    growth_since_start_pct: 20,
  },
  {
    account_id: "a_008",
    account_name: "FinServ Capital",
    csm_id: "csm_002",
    segment: "enterprise",
    current_arr: 580000,
    contract_end_days: 60,
    expansion_type: "cross_sell",
    expansion_readiness: "upcoming",
    churn_signal: "low",
    expansion_action: "schedule_qbr",
    expansion_score: 58.2,
    health_score: 72.4,
    churn_risk_score: 22.0,
    adoption_rate: 65.0,
    feature_utilization: 50.0,
    expansion_potential: 80733.0,
    nrr_forecast: 116.7,
    is_at_risk: false,
    is_ready_to_expand: false,
    active_users: 117,
    licensed_users: 180,
    nps_score: 42,
    whitespace_products: 4,
    growth_since_start_pct: 18,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const readiness = searchParams.get("readiness");
  const churn     = searchParams.get("churn");
  const action    = searchParams.get("action");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/account-expansion`);
      if (readiness) url.searchParams.set("readiness", readiness);
      if (churn)     url.searchParams.set("churn", churn);
      if (action)    url.searchParams.set("action", action);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let accounts = [...mockAccounts];
  if (readiness) accounts = accounts.filter((a) => a.expansion_readiness === readiness);
  if (churn)     accounts = accounts.filter((a) => a.churn_signal === churn);
  if (action)    accounts = accounts.filter((a) => a.expansion_action === action);

  const readiness_counts: Record<string, number> = {};
  const churn_counts:     Record<string, number> = {};
  const action_counts:    Record<string, number> = {};
  let total_health = 0, total_exp = 0, total_churn = 0, total_nrr = 0, total_potential = 0;

  for (const a of mockAccounts) {
    readiness_counts[a.expansion_readiness] = (readiness_counts[a.expansion_readiness] || 0) + 1;
    churn_counts[a.churn_signal]            = (churn_counts[a.churn_signal] || 0) + 1;
    action_counts[a.expansion_action]       = (action_counts[a.expansion_action] || 0) + 1;
    total_health   += a.health_score;
    total_exp      += a.expansion_score;
    total_churn    += a.churn_risk_score;
    total_nrr      += a.nrr_forecast;
    total_potential += a.expansion_potential;
  }

  const n = mockAccounts.length;

  return sealResponse(NextResponse.json({
    accounts,
    summary: {
      total:                        n,
      readiness_counts,
      churn_signal_counts:          churn_counts,
      action_counts,
      expansion_type_counts:        {},
      avg_health_score:             Math.round((total_health / n) * 10) / 10,
      avg_expansion_score:          Math.round((total_exp / n) * 10) / 10,
      avg_churn_risk_score:         Math.round((total_churn / n) * 10) / 10,
      avg_nrr_forecast:             Math.round((total_nrr / n) * 10) / 10,
      total_expansion_potential:    Math.round(total_potential * 100) / 100,
      at_risk_count:                mockAccounts.filter((a) => a.is_at_risk).length,
      ready_to_expand_count:        mockAccounts.filter((a) => a.is_ready_to_expand).length,
      high_value_count:             mockAccounts.filter((a) => a.expansion_potential >= 50000).length,
    },
  }));
}
