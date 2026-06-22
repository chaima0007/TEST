import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[account-expansion-intelligence] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockAccounts = [
  {
    account_id: "acc_001", account_name: "TechCorp Global", rep_id: "rep_001",
    expansion_opportunity: "upsell", expansion_priority: "high",
    account_health: "champion", expansion_action: "schedule_executive_briefing",
    adoption_health_score: 88.0, relationship_health_score: 92.0,
    commercial_readiness_score: 78.0, risk_score: 8.0,
    expansion_composite: 89.2, estimated_expansion_arr_usd: 63750.0,
    is_expansion_ready: true, needs_retention_focus: false,
    primary_expansion_signal: "expansion budget confirmed — ready to propose",
    contract_value_usd: 150000.0, contract_renewal_days: 120, nps_score: 68.0,
  },
  {
    account_id: "acc_002", account_name: "Meridian Finance", rep_id: "rep_002",
    expansion_opportunity: "at_risk", expansion_priority: "critical",
    account_health: "at_risk", expansion_action: "retain_focus",
    adoption_health_score: 18.0, relationship_health_score: 12.0,
    commercial_readiness_score: 5.0, risk_score: 72.0,
    expansion_composite: 23.6, estimated_expansion_arr_usd: 5000.0,
    is_expansion_ready: false, needs_retention_focus: true,
    primary_expansion_signal: "competitor present — displacement opportunity",
    contract_value_usd: 80000.0, contract_renewal_days: 45, nps_score: -42.0,
  },
  {
    account_id: "acc_003", account_name: "Apex Solutions", rep_id: "rep_001",
    expansion_opportunity: "cross_sell", expansion_priority: "high",
    account_health: "healthy", expansion_action: "propose_expansion",
    adoption_health_score: 72.0, relationship_health_score: 68.0,
    commercial_readiness_score: 58.0, risk_score: 15.0,
    expansion_composite: 73.5, estimated_expansion_arr_usd: 42500.0,
    is_expansion_ready: true, needs_retention_focus: false,
    primary_expansion_signal: "3+ product gaps — strong cross-sell potential",
    contract_value_usd: 120000.0, contract_renewal_days: 200, nps_score: 45.0,
  },
  {
    account_id: "acc_004", account_name: "Orion Healthcare", rep_id: "rep_003",
    expansion_opportunity: "renewal_upgrade", expansion_priority: "medium",
    account_health: "stable", expansion_action: "qbr_required",
    adoption_health_score: 52.0, relationship_health_score: 55.0,
    commercial_readiness_score: 45.0, risk_score: 28.0,
    expansion_composite: 57.5, estimated_expansion_arr_usd: 18000.0,
    is_expansion_ready: false, needs_retention_focus: false,
    primary_expansion_signal: "renewal in 90 days — upgrade window open",
    contract_value_usd: 95000.0, contract_renewal_days: 75, nps_score: 22.0,
  },
  {
    account_id: "acc_005", account_name: "Lumina Retail", rep_id: "rep_002",
    expansion_opportunity: "upsell", expansion_priority: "high",
    account_health: "champion", expansion_action: "schedule_executive_briefing",
    adoption_health_score: 92.0, relationship_health_score: 85.0,
    commercial_readiness_score: 82.0, risk_score: 5.0,
    expansion_composite: 91.8, estimated_expansion_arr_usd: 85000.0,
    is_expansion_ready: true, needs_retention_focus: false,
    primary_expansion_signal: "exec sponsor + upsell discussion active",
    contract_value_usd: 200000.0, contract_renewal_days: 160, nps_score: 78.0,
  },
  {
    account_id: "acc_006", account_name: "Cascade Logistics", rep_id: "rep_004",
    expansion_opportunity: "whitespace", expansion_priority: "low",
    account_health: "stable", expansion_action: "qbr_required",
    adoption_health_score: 48.0, relationship_health_score: 42.0,
    commercial_readiness_score: 22.0, risk_score: 32.0,
    expansion_composite: 46.3, estimated_expansion_arr_usd: 8750.0,
    is_expansion_ready: false, needs_retention_focus: false,
    primary_expansion_signal: "standard account nurture required",
    contract_value_usd: 60000.0, contract_renewal_days: 300, nps_score: 12.0,
  },
  {
    account_id: "acc_007", account_name: "Nexus Energy", rep_id: "rep_003",
    expansion_opportunity: "at_risk", expansion_priority: "critical",
    account_health: "at_risk", expansion_action: "retain_focus",
    adoption_health_score: 28.0, relationship_health_score: 22.0,
    commercial_readiness_score: 12.0, risk_score: 65.0,
    expansion_composite: 29.5, estimated_expansion_arr_usd: 2500.0,
    is_expansion_ready: false, needs_retention_focus: true,
    primary_expansion_signal: "competitor present — displacement opportunity",
    contract_value_usd: 110000.0, contract_renewal_days: 35, nps_score: -28.0,
  },
  {
    account_id: "acc_008", account_name: "Vertex Pharma", rep_id: "rep_001",
    expansion_opportunity: "cross_sell", expansion_priority: "medium",
    account_health: "healthy", expansion_action: "propose_expansion",
    adoption_health_score: 65.0, relationship_health_score: 72.0,
    commercial_readiness_score: 55.0, risk_score: 18.0,
    expansion_composite: 70.4, estimated_expansion_arr_usd: 32000.0,
    is_expansion_ready: false, needs_retention_focus: false,
    primary_expansion_signal: "high NPS — strong advocate, expansion ready",
    contract_value_usd: 130000.0, contract_renewal_days: 250, nps_score: 55.0,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const opportunity = searchParams.get("opportunity");
  const priority    = searchParams.get("priority");
  const health      = searchParams.get("health");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/account-expansion-intelligence`);
      if (opportunity) url.searchParams.set("opportunity", opportunity);
      if (priority)    url.searchParams.set("priority", priority);
      if (health)      url.searchParams.set("health", health);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let accounts = [...mockAccounts];
  if (opportunity) accounts = accounts.filter((a) => a.expansion_opportunity === opportunity);
  if (priority)    accounts = accounts.filter((a) => a.expansion_priority === priority);
  if (health)      accounts = accounts.filter((a) => a.account_health === health);

  const opp_counts:  Record<string, number> = {};
  const pri_counts:  Record<string, number> = {};
  const hlth_counts: Record<string, number> = {};
  const act_counts:  Record<string, number> = {};
  let total_comp = 0, total_adopt = 0, total_rel = 0, total_comm = 0, total_risk = 0;
  let total_arr = 0;

  for (const a of mockAccounts) {
    opp_counts[a.expansion_opportunity]  = (opp_counts[a.expansion_opportunity] || 0) + 1;
    pri_counts[a.expansion_priority]     = (pri_counts[a.expansion_priority] || 0) + 1;
    hlth_counts[a.account_health]        = (hlth_counts[a.account_health] || 0) + 1;
    act_counts[a.expansion_action]       = (act_counts[a.expansion_action] || 0) + 1;
    total_comp  += a.expansion_composite;
    total_adopt += a.adoption_health_score;
    total_rel   += a.relationship_health_score;
    total_comm  += a.commercial_readiness_score;
    total_risk  += a.risk_score;
    total_arr   += a.estimated_expansion_arr_usd;
  }

  const n = mockAccounts.length;

  return sealResponse(NextResponse.json({
    accounts,
    summary: {
      total: n,
      opportunity_counts: opp_counts,
      priority_counts: pri_counts,
      health_counts: hlth_counts,
      action_counts: act_counts,
      avg_expansion_composite:          Math.round((total_comp / n) * 10) / 10,
      expansion_ready_count:            mockAccounts.filter((a) => a.is_expansion_ready).length,
      retention_focus_count:            mockAccounts.filter((a) => a.needs_retention_focus).length,
      avg_adoption_health_score:        Math.round((total_adopt / n) * 10) / 10,
      avg_relationship_health_score:    Math.round((total_rel / n) * 10) / 10,
      avg_commercial_readiness_score:   Math.round((total_comm / n) * 10) / 10,
      avg_risk_score:                   Math.round((total_risk / n) * 10) / 10,
      total_expansion_arr_potential_usd: Math.round(total_arr),
    },
  }));
}
