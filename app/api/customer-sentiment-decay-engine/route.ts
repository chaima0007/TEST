import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockAccounts = [
  {
    account_id: "acc_001", account_name: "Meridian Technologies", csm_id: "csm_01", region: "West",
    decay_stage: "stable", decay_risk: "low",
    primary_decay_signal: "none", recommended_action: "no_action",
    engagement_score: 5.0, support_health_score: 4.0, usage_vitality_score: 3.0, relationship_score: 6.0,
    decay_composite: 4.5, is_at_risk: false, requires_escalation: false,
    estimated_arr_at_risk_usd: 5400.0,
    decay_signal: "customer sentiment stable — no decay signals detected",
    contract_value_usd: 120000.0,
  },
  {
    account_id: "acc_002", account_name: "Falcor Systems", csm_id: "csm_01", region: "East",
    decay_stage: "early_warning", decay_risk: "moderate",
    primary_decay_signal: "engagement_drop", recommended_action: "monitor",
    engagement_score: 30.0, support_health_score: 12.0, usage_vitality_score: 18.0, relationship_score: 25.0,
    decay_composite: 21.7, is_at_risk: false, requires_escalation: false,
    estimated_arr_at_risk_usd: 39060.0,
    decay_signal: "no QBR in 5 months — engagement gap — decay composite 22",
    contract_value_usd: 180000.0,
  },
  {
    account_id: "acc_003", account_name: "Quantum Retail Group", csm_id: "csm_02", region: "Central",
    decay_stage: "declining", decay_risk: "moderate",
    primary_decay_signal: "nps_decline", recommended_action: "monitor",
    engagement_score: 38.0, support_health_score: 22.0, usage_vitality_score: 28.0, relationship_score: 18.0,
    decay_composite: 27.5, is_at_risk: false, requires_escalation: false,
    estimated_arr_at_risk_usd: 68750.0,
    decay_signal: "NPS dropped 22pts QoQ (now 28) — decay composite 28",
    contract_value_usd: 250000.0,
  },
  {
    account_id: "acc_004", account_name: "Nexus Financial", csm_id: "csm_02", region: "Southeast",
    decay_stage: "declining", decay_risk: "high",
    primary_decay_signal: "support_escalation", recommended_action: "proactive_outreach",
    engagement_score: 42.0, support_health_score: 70.0, usage_vitality_score: 35.0, relationship_score: 40.0,
    decay_composite: 47.8, is_at_risk: true, requires_escalation: false,
    estimated_arr_at_risk_usd: 238050.0,
    decay_signal: "2 critical ticket(s) in 30 days — 8 total tickets — decay composite 48",
    contract_value_usd: 498000.0,
  },
  {
    account_id: "acc_005", account_name: "Vertex Healthcare", csm_id: "csm_03", region: "Northeast",
    decay_stage: "critical", decay_risk: "critical",
    primary_decay_signal: "executive_silence", recommended_action: "executive_escalation",
    engagement_score: 65.0, support_health_score: 55.0, usage_vitality_score: 72.0, relationship_score: 88.0,
    decay_composite: 69.3, is_at_risk: true, requires_escalation: true,
    estimated_arr_at_risk_usd: 693000.0,
    decay_signal: "zero executive meetings in 90 days (vs 4 prior) — decay composite 69",
    contract_value_usd: 1000000.0,
  },
  {
    account_id: "acc_006", account_name: "Clearwater Energy", csm_id: "csm_03", region: "Northwest",
    decay_stage: "stable", decay_risk: "low",
    primary_decay_signal: "none", recommended_action: "no_action",
    engagement_score: 4.0, support_health_score: 5.0, usage_vitality_score: 2.0, relationship_score: 5.0,
    decay_composite: 4.0, is_at_risk: false, requires_escalation: false,
    estimated_arr_at_risk_usd: 3200.0,
    decay_signal: "customer sentiment stable — no decay signals detected",
    contract_value_usd: 80000.0,
  },
  {
    account_id: "acc_007", account_name: "Pinnacle Logistics", csm_id: "csm_04", region: "Southwest",
    decay_stage: "critical", decay_risk: "high",
    primary_decay_signal: "usage_reduction", recommended_action: "proactive_outreach",
    engagement_score: 30.0, support_health_score: 18.0, usage_vitality_score: 82.0, relationship_score: 52.0,
    decay_composite: 45.4, is_at_risk: true, requires_escalation: false,
    estimated_arr_at_risk_usd: 104420.0,
    decay_signal: "product usage dropped to 22% (from 68%) — decay composite 45",
    contract_value_usd: 230000.0,
  },
  {
    account_id: "acc_008", account_name: "Stratosphere Media", csm_id: "csm_04", region: "Central",
    decay_stage: "churning", decay_risk: "critical",
    primary_decay_signal: "payment_delay", recommended_action: "emergency_intervention",
    engagement_score: 85.0, support_health_score: 78.0, usage_vitality_score: 68.0, relationship_score: 92.0,
    decay_composite: 81.2, is_at_risk: true, requires_escalation: true,
    estimated_arr_at_risk_usd: 365400.0,
    decay_signal: "payment 52 days overdue — decay composite 81",
    contract_value_usd: 450000.0,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const stage = searchParams.get("stage");
  const risk  = searchParams.get("risk");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/customer-sentiment-decay-engine`);
      if (stage) url.searchParams.set("stage", stage);
      if (risk)  url.searchParams.set("risk",  risk);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let accounts = [...mockAccounts];
  if (stage) accounts = accounts.filter((a) => a.decay_stage === stage);
  if (risk)  accounts = accounts.filter((a) => a.decay_risk  === risk);

  const stage_counts:  Record<string, number> = {};
  const risk_counts:   Record<string, number> = {};
  const signal_counts: Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  let total_comp = 0, total_eng = 0, total_sup = 0, total_use = 0, total_rel = 0, total_arr = 0;

  for (const a of mockAccounts) {
    stage_counts[a.decay_stage]           = (stage_counts[a.decay_stage] || 0) + 1;
    risk_counts[a.decay_risk]             = (risk_counts[a.decay_risk] || 0) + 1;
    signal_counts[a.primary_decay_signal] = (signal_counts[a.primary_decay_signal] || 0) + 1;
    action_counts[a.recommended_action]   = (action_counts[a.recommended_action] || 0) + 1;
    total_comp += a.decay_composite;
    total_eng  += a.engagement_score;
    total_sup  += a.support_health_score;
    total_use  += a.usage_vitality_score;
    total_rel  += a.relationship_score;
    total_arr  += a.estimated_arr_at_risk_usd;
  }

  const n = mockAccounts.length;

  return NextResponse.json(sealResponse({
    accounts,
    summary: {
      total:                      n,
      stage_counts,
      risk_counts,
      signal_counts,
      action_counts,
      avg_decay_composite:        Math.round((total_comp / n) * 10) / 10,
      at_risk_count:              mockAccounts.filter((a) => a.is_at_risk).length,
      escalation_count:           mockAccounts.filter((a) => a.requires_escalation).length,
      avg_engagement_score:       Math.round((total_eng  / n) * 10) / 10,
      avg_support_health_score:   Math.round((total_sup  / n) * 10) / 10,
      avg_usage_vitality_score:   Math.round((total_use  / n) * 10) / 10,
      avg_relationship_score:     Math.round((total_rel  / n) * 10) / 10,
      total_arr_at_risk_usd:      Math.round(total_arr),
    },
  } as Record<string,unknown>));
}
