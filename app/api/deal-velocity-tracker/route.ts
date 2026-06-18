import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "deal_001", deal_name: "Acme Corp Enterprise", rep_id: "rep_003",
    velocity_status: "accelerating", slip_risk: "low", deal_momentum: "strong",
    velocity_action: "maintain",
    stage_progress_score: 88.0, activity_velocity_score: 92.0,
    stakeholder_momentum_score: 85.0, urgency_alignment_score: 90.0,
    velocity_composite: 89.8, days_in_current_stage: 5,
    close_date_push_count: 0, is_on_track: true,
    needs_velocity_boost: false, region: "NAMER",
  },
  {
    deal_id: "deal_002", deal_name: "BetaTech Renewal", rep_id: "rep_001",
    velocity_status: "stalled", slip_risk: "critical", deal_momentum: "lost",
    velocity_action: "rescue",
    stage_progress_score: 10.0, activity_velocity_score: 8.0,
    stakeholder_momentum_score: 12.0, urgency_alignment_score: 5.0,
    velocity_composite: 9.1, days_in_current_stage: 45,
    close_date_push_count: 3, is_on_track: false,
    needs_velocity_boost: true, region: "EMEA",
  },
  {
    deal_id: "deal_003", deal_name: "CloudBase SaaS", rep_id: "rep_002",
    velocity_status: "on_pace", slip_risk: "low", deal_momentum: "building",
    velocity_action: "maintain",
    stage_progress_score: 65.0, activity_velocity_score: 60.0,
    stakeholder_momentum_score: 58.0, urgency_alignment_score: 55.0,
    velocity_composite: 61.0, days_in_current_stage: 12,
    close_date_push_count: 1, is_on_track: true,
    needs_velocity_boost: false, region: "APAC",
  },
  {
    deal_id: "deal_004", deal_name: "Delta Systems", rep_id: "rep_005",
    velocity_status: "decelerating", slip_risk: "high", deal_momentum: "fading",
    velocity_action: "inject_urgency",
    stage_progress_score: 32.0, activity_velocity_score: 25.0,
    stakeholder_momentum_score: 28.0, urgency_alignment_score: 20.0,
    velocity_composite: 27.2, days_in_current_stage: 28,
    close_date_push_count: 2, is_on_track: false,
    needs_velocity_boost: true, region: "NAMER",
  },
  {
    deal_id: "deal_005", deal_name: "EcoTech Green", rep_id: "rep_007",
    velocity_status: "accelerating", slip_risk: "low", deal_momentum: "strong",
    velocity_action: "accelerate",
    stage_progress_score: 78.0, activity_velocity_score: 82.0,
    stakeholder_momentum_score: 75.0, urgency_alignment_score: 80.0,
    velocity_composite: 79.7, days_in_current_stage: 7,
    close_date_push_count: 0, is_on_track: true,
    needs_velocity_boost: false, region: "EMEA",
  },
  {
    deal_id: "deal_006", deal_name: "Finova Capital", rep_id: "rep_004",
    velocity_status: "on_pace", slip_risk: "moderate", deal_momentum: "building",
    velocity_action: "maintain",
    stage_progress_score: 52.0, activity_velocity_score: 48.0,
    stakeholder_momentum_score: 50.0, urgency_alignment_score: 45.0,
    velocity_composite: 49.8, days_in_current_stage: 18,
    close_date_push_count: 1, is_on_track: false,
    needs_velocity_boost: false, region: "APAC",
  },
  {
    deal_id: "deal_007", deal_name: "GlobalLink Networks", rep_id: "rep_006",
    velocity_status: "accelerating", slip_risk: "low", deal_momentum: "strong",
    velocity_action: "maintain",
    stage_progress_score: 85.0, activity_velocity_score: 90.0,
    stakeholder_momentum_score: 88.0, urgency_alignment_score: 82.0,
    velocity_composite: 87.2, days_in_current_stage: 6,
    close_date_push_count: 0, is_on_track: true,
    needs_velocity_boost: false, region: "LATAM",
  },
  {
    deal_id: "deal_008", deal_name: "HorizonAI Platform", rep_id: "rep_008",
    velocity_status: "stalled", slip_risk: "critical", deal_momentum: "lost",
    velocity_action: "rescue",
    stage_progress_score: 15.0, activity_velocity_score: 10.0,
    stakeholder_momentum_score: 18.0, urgency_alignment_score: 8.0,
    velocity_composite: 12.9, days_in_current_stage: 38,
    close_date_push_count: 4, is_on_track: false,
    needs_velocity_boost: true, region: "NAMER",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const status   = searchParams.get("status");
  const slip     = searchParams.get("slip");
  const region   = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/deal-velocity-tracker`);
      if (status) url.searchParams.set("status", status);
      if (slip)   url.searchParams.set("slip", slip);
      if (region) url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let deals = [...mockDeals];
  if (status) deals = deals.filter((d) => d.velocity_status === status);
  if (slip)   deals = deals.filter((d) => d.slip_risk === slip);
  if (region) deals = deals.filter((d) => d.region === region);

  const status_counts:   Record<string, number> = {};
  const slip_counts:     Record<string, number> = {};
  const momentum_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_stage = 0, total_activity = 0,
      total_stkh = 0, total_urg = 0;

  for (const d of mockDeals) {
    status_counts[d.velocity_status]   = (status_counts[d.velocity_status] || 0) + 1;
    slip_counts[d.slip_risk]           = (slip_counts[d.slip_risk] || 0) + 1;
    momentum_counts[d.deal_momentum]   = (momentum_counts[d.deal_momentum] || 0) + 1;
    action_counts[d.velocity_action]   = (action_counts[d.velocity_action] || 0) + 1;
    total_comp     += d.velocity_composite;
    total_stage    += d.stage_progress_score;
    total_activity += d.activity_velocity_score;
    total_stkh     += d.stakeholder_momentum_score;
    total_urg      += d.urgency_alignment_score;
  }

  const n = mockDeals.length;

  return NextResponse.json({
    deals,
    summary: {
      total: n,
      status_counts,
      slip_counts,
      momentum_counts,
      action_counts,
      avg_velocity_composite:         Math.round((total_comp / n) * 10) / 10,
      on_track_count:                 mockDeals.filter((d) => d.is_on_track).length,
      boost_needed_count:             mockDeals.filter((d) => d.needs_velocity_boost).length,
      avg_stage_progress_score:       Math.round((total_stage / n) * 10) / 10,
      avg_activity_velocity_score:    Math.round((total_activity / n) * 10) / 10,
      avg_stakeholder_momentum_score: Math.round((total_stkh / n) * 10) / 10,
      avg_urgency_alignment_score:    Math.round((total_urg / n) * 10) / 10,
    },
  });
}
