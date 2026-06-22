import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[customer-onboarding] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockAccounts = [
  {
    account_id: "ob_001",
    account_name: "TechCorp SA",
    csm_id: "csm_001",
    segment: "enterprise",
    current_phase: "adoption",
    onboarding_risk: "low",
    success_probability: "high",
    onboarding_action: "accelerate",
    completion_score: 85.0,
    time_to_value_score: 90.0,
    adoption_velocity: 8.0,
    training_completion_rate: 80.0,
    integration_health: 100.0,
    risk_flags_count: 0,
    is_on_track: true,
    is_at_risk: false,
    contract_start_days: 15,
    expected_onboarding_days: 45,
    users_activated: 40,
    users_licensed: 50,
  },
  {
    account_id: "ob_002",
    account_name: "GlobalFinance SARL",
    csm_id: "csm_002",
    segment: "enterprise",
    current_phase: "configuration",
    onboarding_risk: "critical",
    success_probability: "at_risk",
    onboarding_action: "intervene",
    completion_score: 22.0,
    time_to_value_score: 18.0,
    adoption_velocity: 1.5,
    training_completion_rate: 25.0,
    integration_health: 33.3,
    risk_flags_count: 5,
    is_on_track: false,
    is_at_risk: true,
    contract_start_days: 75,
    expected_onboarding_days: 45,
    users_activated: 8,
    users_licensed: 60,
  },
  {
    account_id: "ob_003",
    account_name: "MediaGroup SAS",
    csm_id: "csm_001",
    segment: "mid_market",
    current_phase: "training",
    onboarding_risk: "medium",
    success_probability: "medium",
    onboarding_action: "standard",
    completion_score: 58.0,
    time_to_value_score: 62.0,
    adoption_velocity: 4.5,
    training_completion_rate: 60.0,
    integration_health: 66.7,
    risk_flags_count: 2,
    is_on_track: false,
    is_at_risk: false,
    contract_start_days: 22,
    expected_onboarding_days: 30,
    users_activated: 18,
    users_licensed: 40,
  },
  {
    account_id: "ob_004",
    account_name: "HealthTech Pro",
    csm_id: "csm_003",
    segment: "enterprise",
    current_phase: "complete",
    onboarding_risk: "low",
    success_probability: "high",
    onboarding_action: "celebrate",
    completion_score: 96.0,
    time_to_value_score: 88.0,
    adoption_velocity: 7.5,
    training_completion_rate: 100.0,
    integration_health: 100.0,
    risk_flags_count: 0,
    is_on_track: true,
    is_at_risk: false,
    contract_start_days: 42,
    expected_onboarding_days: 45,
    users_activated: 90,
    users_licensed: 100,
  },
  {
    account_id: "ob_005",
    account_name: "RetailChain Nord",
    csm_id: "csm_002",
    segment: "mid_market",
    current_phase: "kickoff",
    onboarding_risk: "high",
    success_probability: "low",
    onboarding_action: "reassign",
    completion_score: 35.0,
    time_to_value_score: 28.0,
    adoption_velocity: 1.0,
    training_completion_rate: 0.0,
    integration_health: 0.0,
    risk_flags_count: 4,
    is_on_track: false,
    is_at_risk: true,
    contract_start_days: 18,
    expected_onboarding_days: 30,
    users_activated: 3,
    users_licensed: 50,
  },
  {
    account_id: "ob_006",
    account_name: "LogisticsPlus SA",
    csm_id: "csm_003",
    segment: "mid_market",
    current_phase: "value_realization",
    onboarding_risk: "low",
    success_probability: "high",
    onboarding_action: "accelerate",
    completion_score: 78.0,
    time_to_value_score: 82.0,
    adoption_velocity: 6.2,
    training_completion_rate: 100.0,
    integration_health: 75.0,
    risk_flags_count: 1,
    is_on_track: true,
    is_at_risk: false,
    contract_start_days: 30,
    expected_onboarding_days: 45,
    users_activated: 31,
    users_licensed: 50,
  },
  {
    account_id: "ob_007",
    account_name: "EduSmart Group",
    csm_id: "csm_001",
    segment: "smb",
    current_phase: "adoption",
    onboarding_risk: "medium",
    success_probability: "medium",
    onboarding_action: "standard",
    completion_score: 62.0,
    time_to_value_score: 55.0,
    adoption_velocity: 3.0,
    training_completion_rate: 75.0,
    integration_health: 100.0,
    risk_flags_count: 2,
    is_on_track: false,
    is_at_risk: false,
    contract_start_days: 20,
    expected_onboarding_days: 21,
    users_activated: 12,
    users_licensed: 30,
  },
  {
    account_id: "ob_008",
    account_name: "FinServ Capital",
    csm_id: "csm_002",
    segment: "enterprise",
    current_phase: "configuration",
    onboarding_risk: "high",
    success_probability: "low",
    onboarding_action: "escalate",
    completion_score: 44.0,
    time_to_value_score: 35.0,
    adoption_velocity: 2.8,
    training_completion_rate: 40.0,
    integration_health: 50.0,
    risk_flags_count: 3,
    is_on_track: false,
    is_at_risk: true,
    contract_start_days: 55,
    expected_onboarding_days: 60,
    users_activated: 28,
    users_licensed: 180,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const phase  = searchParams.get("phase");
  const risk   = searchParams.get("risk");
  const action = searchParams.get("action");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/customer-onboarding`);
      if (phase)  url.searchParams.set("phase", phase);
      if (risk)   url.searchParams.set("risk", risk);
      if (action) url.searchParams.set("action", action);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let accounts = [...mockAccounts];
  if (phase)  accounts = accounts.filter((a) => a.current_phase === phase);
  if (risk)   accounts = accounts.filter((a) => a.onboarding_risk === risk);
  if (action) accounts = accounts.filter((a) => a.onboarding_action === action);

  const phase_counts:  Record<string, number> = {};
  const risk_counts:   Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  let total_completion = 0, total_ttv = 0, total_velocity = 0;

  for (const a of mockAccounts) {
    phase_counts[a.current_phase]    = (phase_counts[a.current_phase] || 0) + 1;
    risk_counts[a.onboarding_risk]   = (risk_counts[a.onboarding_risk] || 0) + 1;
    action_counts[a.onboarding_action] = (action_counts[a.onboarding_action] || 0) + 1;
    total_completion += a.completion_score;
    total_ttv        += a.time_to_value_score;
    total_velocity   += a.adoption_velocity;
  }

  const n = mockAccounts.length;

  return sealResponse(NextResponse.json({
    accounts,
    summary: {
      total:                   n,
      phase_counts,
      risk_counts,
      action_counts,
      avg_completion_score:    Math.round((total_completion / n) * 10) / 10,
      avg_time_to_value_score: Math.round((total_ttv / n) * 10) / 10,
      avg_adoption_velocity:   Math.round((total_velocity / n) * 100) / 100,
      at_risk_count:           mockAccounts.filter((a) => a.is_at_risk).length,
      on_track_count:          mockAccounts.filter((a) => a.is_on_track).length,
      critical_count:          mockAccounts.filter((a) => a.onboarding_risk === "critical").length,
      high_success_count:      mockAccounts.filter((a) => a.success_probability === "high").length,
      escalation_needed_count: mockAccounts.filter(
        (a) => a.onboarding_action === "escalate" || a.onboarding_action === "intervene"
      ).length,
    },
  }));
}
