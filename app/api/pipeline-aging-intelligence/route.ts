import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "deal_001", rep_id: "rep_001", deal_name: "Acme Corp Enterprise",
    decay_status: "fresh", decay_risk: "low",
    stage_velocity: "fast", recovery_action: "maintain",
    activity_decay_score: 5.0, engagement_decay_score: 0.0,
    velocity_decay_score: 0.0, stage_health_score: 80.0,
    decay_composite: 1.2, is_stale: false, needs_immediate_action: false,
    recovery_probability_pct: 98.8, deal_value_usd: 180000.0, deal_stage: 3,
    primary_decay_signal: "primary decay driver: activity decay",
  },
  {
    deal_id: "deal_002", rep_id: "rep_002", deal_name: "Meridian Finance Q3",
    decay_status: "dead", decay_risk: "critical",
    stage_velocity: "stalled", recovery_action: "kill_or_recycle",
    activity_decay_score: 85.0, engagement_decay_score: 90.0,
    velocity_decay_score: 78.0, stage_health_score: 5.0,
    decay_composite: 87.3, is_stale: true, needs_immediate_action: true,
    recovery_probability_pct: 12.7, deal_value_usd: 250000.0, deal_stage: 2,
    primary_decay_signal: "buyer dark for 35 days — deal may be lost",
  },
  {
    deal_id: "deal_003", rep_id: "rep_001", deal_name: "Vertex Pharma Expansion",
    decay_status: "aging", decay_risk: "moderate",
    stage_velocity: "slow", recovery_action: "re_engage_champion",
    activity_decay_score: 32.0, engagement_decay_score: 28.0,
    velocity_decay_score: 30.0, stage_health_score: 42.0,
    decay_composite: 37.2, is_stale: false, needs_immediate_action: false,
    recovery_probability_pct: 62.8, deal_value_usd: 135000.0, deal_stage: 1,
    primary_decay_signal: "primary decay driver: velocity decay",
  },
  {
    deal_id: "deal_004", rep_id: "rep_003", deal_name: "Lumina Retail Platform",
    decay_status: "stale", decay_risk: "high",
    stage_velocity: "stalled", recovery_action: "executive_escalation",
    activity_decay_score: 60.0, engagement_decay_score: 55.0,
    velocity_decay_score: 52.0, stage_health_score: 18.0,
    decay_composite: 62.1, is_stale: true, needs_immediate_action: false,
    recovery_probability_pct: 37.9, deal_value_usd: 195000.0, deal_stage: 3,
    primary_decay_signal: "champion not engaged in 22 days — internal advocate at risk",
  },
  {
    deal_id: "deal_005", rep_id: "rep_004", deal_name: "TechCorp Global Renewal",
    decay_status: "fresh", decay_risk: "low",
    stage_velocity: "fast", recovery_action: "maintain",
    activity_decay_score: 0.0, engagement_decay_score: 0.0,
    velocity_decay_score: 0.0, stage_health_score: 95.0,
    decay_composite: 1.0, is_stale: false, needs_immediate_action: false,
    recovery_probability_pct: 99.0, deal_value_usd: 300000.0, deal_stage: 4,
    primary_decay_signal: "primary decay driver: stage health gap",
  },
  {
    deal_id: "deal_006", rep_id: "rep_002", deal_name: "Cascade Logistics EMEA",
    decay_status: "stale", decay_risk: "high",
    stage_velocity: "slow", recovery_action: "executive_escalation",
    activity_decay_score: 55.0, engagement_decay_score: 60.0,
    velocity_decay_score: 48.0, stage_health_score: 15.0,
    decay_composite: 60.2, is_stale: true, needs_immediate_action: false,
    recovery_probability_pct: 39.8, deal_value_usd: 115000.0, deal_stage: 2,
    primary_decay_signal: "close date pushed 4 times — buyer commitment weak",
  },
  {
    deal_id: "deal_007", rep_id: "rep_003", deal_name: "Nexus Energy Cloud",
    decay_status: "aging", decay_risk: "moderate",
    stage_velocity: "on_track", recovery_action: "re_engage_champion",
    activity_decay_score: 28.0, engagement_decay_score: 22.0,
    velocity_decay_score: 18.0, stage_health_score: 55.0,
    decay_composite: 30.4, is_stale: false, needs_immediate_action: false,
    recovery_probability_pct: 69.6, deal_value_usd: 160000.0, deal_stage: 2,
    primary_decay_signal: "primary decay driver: activity decay",
  },
  {
    deal_id: "deal_008", rep_id: "rep_004", deal_name: "Orion Healthcare Suite",
    decay_status: "dead", decay_risk: "critical",
    stage_velocity: "stalled", recovery_action: "kill_or_recycle",
    activity_decay_score: 90.0, engagement_decay_score: 85.0,
    velocity_decay_score: 80.0, stage_health_score: 0.0,
    decay_composite: 91.3, is_stale: true, needs_immediate_action: true,
    recovery_probability_pct: 8.7, deal_value_usd: 220000.0, deal_stage: 3,
    primary_decay_signal: "no rep activity for 28 days — deal abandoned",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const status = searchParams.get("status");
  const risk   = searchParams.get("risk");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/pipeline-aging-intelligence`);
      if (status) url.searchParams.set("status", status);
      if (risk)   url.searchParams.set("risk", risk);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let deals = [...mockDeals];
  if (status) deals = deals.filter((d) => d.decay_status === status);
  if (risk)   deals = deals.filter((d) => d.decay_risk === risk);

  const status_counts: Record<string, number> = {};
  const risk_counts:   Record<string, number> = {};
  const vel_counts:    Record<string, number> = {};
  const act_counts:    Record<string, number> = {};
  let total_comp = 0, total_act = 0, total_eng = 0, total_vel = 0, total_sh = 0;
  let total_stale_pipe = 0;

  for (const d of mockDeals) {
    status_counts[d.decay_status]    = (status_counts[d.decay_status] || 0) + 1;
    risk_counts[d.decay_risk]        = (risk_counts[d.decay_risk] || 0) + 1;
    vel_counts[d.stage_velocity]     = (vel_counts[d.stage_velocity] || 0) + 1;
    act_counts[d.recovery_action]    = (act_counts[d.recovery_action] || 0) + 1;
    total_comp += d.decay_composite;
    total_act  += d.activity_decay_score;
    total_eng  += d.engagement_decay_score;
    total_vel  += d.velocity_decay_score;
    total_sh   += d.stage_health_score;
    if (d.is_stale) total_stale_pipe += d.deal_value_usd;
  }

  const n = mockDeals.length;

  return NextResponse.json({
    deals,
    summary: {
      total: n,
      decay_status_counts: status_counts,
      risk_counts,
      velocity_counts: vel_counts,
      action_counts: act_counts,
      avg_decay_composite:          Math.round((total_comp / n) * 10) / 10,
      stale_deal_count:             mockDeals.filter((d) => d.is_stale).length,
      immediate_action_count:       mockDeals.filter((d) => d.needs_immediate_action).length,
      avg_activity_decay_score:     Math.round((total_act / n) * 10) / 10,
      avg_engagement_decay_score:   Math.round((total_eng / n) * 10) / 10,
      avg_velocity_decay_score:     Math.round((total_vel / n) * 10) / 10,
      avg_stage_health_score:       Math.round((total_sh / n) * 10) / 10,
      total_stale_pipeline_usd:     Math.round(total_stale_pipe * 100) / 100,
    },
  });
}
