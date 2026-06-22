import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[deal-velocity] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "d_001", deal_name: "Acme Corp CRM Expansion", rep_id: "r_001",
    account_id: "a_001", stage_number: 4, deal_value: 180000,
    velocity_trend: "accelerating", stage_health: "healthy",
    deal_outcome: "likely_close", velocity_action: "accelerate",
    velocity_score: 82.0, stage_progression_rate: 1.6, close_date_risk: 12.0,
    engagement_score: 90.0, momentum_score: 78.0, deal_health_index: 83.4,
    is_at_risk: false, needs_escalation: false,
    probability_pct: 78.0, expected_close_days: 9, last_activity_days_ago: 1,
    competitor_present: false, decision_maker_engaged: true, champion_identified: true,
    nrr_expansion_potential: 40000,
  },
  {
    deal_id: "d_002", deal_name: "Brightside Tech Platform", rep_id: "r_002",
    account_id: "a_002", stage_number: 3, deal_value: 95000,
    velocity_trend: "stable", stage_health: "slow",
    deal_outcome: "on_track", velocity_action: "standard_follow_up",
    velocity_score: 61.0, stage_progression_rate: 0.9, close_date_risk: 22.0,
    engagement_score: 70.0, momentum_score: 55.0, deal_health_index: 61.8,
    is_at_risk: false, needs_escalation: false,
    probability_pct: 62.0, expected_close_days: 21, last_activity_days_ago: 4,
    competitor_present: false, decision_maker_engaged: true, champion_identified: false,
    nrr_expansion_potential: 18000,
  },
  {
    deal_id: "d_003", deal_name: "CloudNine Infrastructure", rep_id: "r_003",
    account_id: "a_003", stage_number: 2, deal_value: 240000,
    velocity_trend: "decelerating", stage_health: "stuck",
    deal_outcome: "at_risk", velocity_action: "prioritize",
    velocity_score: 38.0, stage_progression_rate: 0.62, close_date_risk: 48.0,
    engagement_score: 50.0, momentum_score: 34.0, deal_health_index: 40.5,
    is_at_risk: true, needs_escalation: false,
    probability_pct: 40.0, expected_close_days: 35, last_activity_days_ago: 12,
    competitor_present: true, decision_maker_engaged: false, champion_identified: true,
    nrr_expansion_potential: 60000,
  },
  {
    deal_id: "d_004", deal_name: "DataStream Analytics Suite", rep_id: "r_001",
    account_id: "a_004", stage_number: 5, deal_value: 320000,
    velocity_trend: "accelerating", stage_health: "healthy",
    deal_outcome: "likely_close", velocity_action: "accelerate",
    velocity_score: 88.0, stage_progression_rate: 1.8, close_date_risk: 8.0,
    engagement_score: 100.0, momentum_score: 84.0, deal_health_index: 90.2,
    is_at_risk: false, needs_escalation: false,
    probability_pct: 88.0, expected_close_days: 5, last_activity_days_ago: 0,
    competitor_present: false, decision_maker_engaged: true, champion_identified: true,
    nrr_expansion_potential: 80000,
  },
  {
    deal_id: "d_005", deal_name: "EchoSoft Renewal + Upsell", rep_id: "r_004",
    account_id: "a_005", stage_number: 3, deal_value: 75000,
    velocity_trend: "stalled", stage_health: "critical",
    deal_outcome: "likely_slip", velocity_action: "engage_executive",
    velocity_score: 22.0, stage_progression_rate: 0.28, close_date_risk: 74.0,
    engagement_score: 30.0, momentum_score: 20.0, deal_health_index: 23.8,
    is_at_risk: true, needs_escalation: true,
    probability_pct: 28.0, expected_close_days: 3, last_activity_days_ago: 25,
    competitor_present: true, decision_maker_engaged: false, champion_identified: false,
    nrr_expansion_potential: 12000,
  },
  {
    deal_id: "d_006", deal_name: "Frontwave Security Bundle", rep_id: "r_002",
    account_id: "a_006", stage_number: 4, deal_value: 155000,
    velocity_trend: "stable", stage_health: "healthy",
    deal_outcome: "on_track", velocity_action: "standard_follow_up",
    velocity_score: 68.0, stage_progression_rate: 1.1, close_date_risk: 18.0,
    engagement_score: 75.0, momentum_score: 62.0, deal_health_index: 68.0,
    is_at_risk: false, needs_escalation: false,
    probability_pct: 65.0, expected_close_days: 18, last_activity_days_ago: 3,
    competitor_present: false, decision_maker_engaged: true, champion_identified: true,
    nrr_expansion_potential: 30000,
  },
  {
    deal_id: "d_007", deal_name: "GreenPath Logistics Pilot", rep_id: "r_003",
    account_id: "a_007", stage_number: 2, deal_value: 48000,
    velocity_trend: "decelerating", stage_health: "stuck",
    deal_outcome: "likely_lose", velocity_action: "reassign",
    velocity_score: 18.0, stage_progression_rate: 0.45, close_date_risk: 65.0,
    engagement_score: 20.0, momentum_score: 16.0, deal_health_index: 17.9,
    is_at_risk: true, needs_escalation: true,
    probability_pct: 18.0, expected_close_days: 45, last_activity_days_ago: 18,
    competitor_present: true, decision_maker_engaged: false, champion_identified: false,
    nrr_expansion_potential: 5000,
  },
  {
    deal_id: "d_008", deal_name: "Highpoint HQ Enterprise", rep_id: "r_004",
    account_id: "a_008", stage_number: 3, deal_value: 210000,
    velocity_trend: "stable", stage_health: "slow",
    deal_outcome: "at_risk", velocity_action: "prioritize",
    velocity_score: 44.0, stage_progression_rate: 0.75, close_date_risk: 38.0,
    engagement_score: 55.0, momentum_score: 40.0, deal_health_index: 45.7,
    is_at_risk: true, needs_escalation: false,
    probability_pct: 45.0, expected_close_days: 28, last_activity_days_ago: 8,
    competitor_present: true, decision_maker_engaged: true, champion_identified: false,
    nrr_expansion_potential: 45000,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const trend   = searchParams.get("trend");
  const outcome = searchParams.get("outcome");
  const rep_id  = searchParams.get("rep_id");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/deal-velocity`);
      if (trend)   url.searchParams.set("trend", trend);
      if (outcome) url.searchParams.set("outcome", outcome);
      if (rep_id)  url.searchParams.set("rep_id", rep_id);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let deals = [...mockDeals];
  if (trend)   deals = deals.filter((d) => d.velocity_trend === trend);
  if (outcome) deals = deals.filter((d) => d.deal_outcome === outcome);
  if (rep_id)  deals = deals.filter((d) => d.rep_id === rep_id);

  const trend_counts:   Record<string, number> = {};
  const health_counts:  Record<string, number> = {};
  const outcome_counts: Record<string, number> = {};
  const action_counts:  Record<string, number> = {};
  let total_velocity = 0, total_health = 0, total_risk = 0,
      total_engagement = 0, total_momentum = 0;

  for (const d of mockDeals) {
    trend_counts[d.velocity_trend]   = (trend_counts[d.velocity_trend] || 0) + 1;
    health_counts[d.stage_health]    = (health_counts[d.stage_health] || 0) + 1;
    outcome_counts[d.deal_outcome]   = (outcome_counts[d.deal_outcome] || 0) + 1;
    action_counts[d.velocity_action] = (action_counts[d.velocity_action] || 0) + 1;
    total_velocity   += d.velocity_score;
    total_health     += d.deal_health_index;
    total_risk       += d.close_date_risk;
    total_engagement += d.engagement_score;
    total_momentum   += d.momentum_score;
  }

  const n = mockDeals.length;

  return sealResponse(NextResponse.json({
    deals,
    summary: {
      total:                   n,
      trend_counts,
      health_counts,
      outcome_counts,
      action_counts,
      avg_velocity_score:      Math.round((total_velocity / n) * 10) / 10,
      avg_deal_health_index:   Math.round((total_health / n) * 10) / 10,
      avg_close_date_risk:     Math.round((total_risk / n) * 10) / 10,
      at_risk_count:           mockDeals.filter((d) => d.is_at_risk).length,
      escalation_count:        mockDeals.filter((d) => d.needs_escalation).length,
      avg_engagement_score:    Math.round((total_engagement / n) * 10) / 10,
      avg_momentum_score:      Math.round((total_momentum / n) * 10) / 10,
      healthy_deal_count:      mockDeals.filter((d) => d.deal_health_index >= 65.0).length,
    },
  }));
}
