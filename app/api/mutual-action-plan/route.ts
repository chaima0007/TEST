import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockMAPs = [
  {
    deal_id: "deal_001", deal_name: "Apex Cloud Platform", rep_id: "rep_003",
    map_health: "on_track", adherence_pattern: "both_committed",
    commitment_signal: "strong", map_action: "accelerate",
    rep_adherence_score: 100.0, buyer_adherence_score: 90.0,
    milestone_progress_score: 88.0, map_quality_score: 93.0,
    map_adherence_composite: 91.8, estimated_close_confidence: 95.0,
    days_to_close_risk: 0, is_healthy_map: true, needs_map_reset: false,
    deal_value: 400000, region: "NAMER",
  },
  {
    deal_id: "deal_002", deal_name: "Solaris Data Platform", rep_id: "rep_001",
    map_health: "broken", adherence_pattern: "buyer_ghosting",
    commitment_signal: "absent", map_action: "escalate",
    rep_adherence_score: 80.0, buyer_adherence_score: 15.0,
    milestone_progress_score: 22.0, map_quality_score: 55.0,
    map_adherence_composite: 38.3, estimated_close_confidence: 14.0,
    days_to_close_risk: 74, is_healthy_map: false, needs_map_reset: true,
    deal_value: 300000, region: "EMEA",
  },
  {
    deal_id: "deal_003", deal_name: "ZenithAI Scale-Up", rep_id: "rep_002",
    map_health: "on_track", adherence_pattern: "both_committed",
    commitment_signal: "strong", map_action: "accelerate",
    rep_adherence_score: 90.0, buyer_adherence_score: 85.0,
    milestone_progress_score: 75.0, map_quality_score: 80.0,
    map_adherence_composite: 82.5, estimated_close_confidence: 88.0,
    days_to_close_risk: 0, is_healthy_map: true, needs_map_reset: false,
    deal_value: 200000, region: "APAC",
  },
  {
    deal_id: "deal_004", deal_name: "Harbor Security Suite", rep_id: "rep_005",
    map_health: "slipping", adherence_pattern: "rep_only",
    commitment_signal: "weak", map_action: "reaffirm",
    rep_adherence_score: 80.0, buyer_adherence_score: 32.0,
    milestone_progress_score: 52.0, map_quality_score: 60.0,
    map_adherence_composite: 54.7, estimated_close_confidence: 42.0,
    days_to_close_risk: 28, is_healthy_map: false, needs_map_reset: false,
    deal_value: 500000, region: "NAMER",
  },
  {
    deal_id: "deal_005", deal_name: "PeakFlow Analytics", rep_id: "rep_007",
    map_health: "at_risk", adherence_pattern: "mutual_drift",
    commitment_signal: "weak", map_action: "reset_map",
    rep_adherence_score: 45.0, buyer_adherence_score: 38.0,
    milestone_progress_score: 30.0, map_quality_score: 45.0,
    map_adherence_composite: 38.8, estimated_close_confidence: 28.0,
    days_to_close_risk: 56, is_healthy_map: false, needs_map_reset: false,
    deal_value: 230000, region: "EMEA",
  },
  {
    deal_id: "deal_006", deal_name: "Orbit ERP Integration", rep_id: "rep_004",
    map_health: "broken", adherence_pattern: "complete_breakdown",
    commitment_signal: "absent", map_action: "escalate",
    rep_adherence_score: 20.0, buyer_adherence_score: 18.0,
    milestone_progress_score: 15.0, map_quality_score: 30.0,
    map_adherence_composite: 19.5, estimated_close_confidence: 8.0,
    days_to_close_risk: 90, is_healthy_map: false, needs_map_reset: true,
    deal_value: 180000, region: "APAC",
  },
  {
    deal_id: "deal_007", deal_name: "Nexus Platform Expansion", rep_id: "rep_006",
    map_health: "on_track", adherence_pattern: "buyer_leading",
    commitment_signal: "moderate", map_action: "accelerate",
    rep_adherence_score: 48.0, buyer_adherence_score: 78.0,
    milestone_progress_score: 65.0, map_quality_score: 70.0,
    map_adherence_composite: 65.2, estimated_close_confidence: 72.0,
    days_to_close_risk: 0, is_healthy_map: true, needs_map_reset: false,
    deal_value: 180000, region: "LATAM",
  },
  {
    deal_id: "deal_008", deal_name: "Vertex CX Rollout", rep_id: "rep_008",
    map_health: "slipping", adherence_pattern: "mutual_drift",
    commitment_signal: "weak", map_action: "reaffirm",
    rep_adherence_score: 55.0, buyer_adherence_score: 45.0,
    milestone_progress_score: 48.0, map_quality_score: 50.0,
    map_adherence_composite: 48.8, estimated_close_confidence: 38.0,
    days_to_close_risk: 14, is_healthy_map: false, needs_map_reset: false,
    deal_value: 190000, region: "NAMER",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const health  = searchParams.get("health");
  const pattern = searchParams.get("pattern");
  const region  = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/mutual-action-plan`);
      if (health)  url.searchParams.set("health", health);
      if (pattern) url.searchParams.set("pattern", pattern);
      if (region)  url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let maps = [...mockMAPs];
  if (health)  maps = maps.filter((m) => m.map_health === health);
  if (pattern) maps = maps.filter((m) => m.adherence_pattern === pattern);
  if (region)  maps = maps.filter((m) => m.region === region);

  const health_counts:  Record<string, number> = {};
  const pattern_counts: Record<string, number> = {};
  const signal_counts:  Record<string, number> = {};
  const action_counts:  Record<string, number> = {};
  let total_comp = 0, total_conf = 0, total_rep = 0,
      total_buy = 0, total_mile = 0, total_qual = 0;

  for (const m of mockMAPs) {
    health_counts[m.map_health]           = (health_counts[m.map_health] || 0) + 1;
    pattern_counts[m.adherence_pattern]   = (pattern_counts[m.adherence_pattern] || 0) + 1;
    signal_counts[m.commitment_signal]    = (signal_counts[m.commitment_signal] || 0) + 1;
    action_counts[m.map_action]           = (action_counts[m.map_action] || 0) + 1;
    total_comp += m.map_adherence_composite;
    total_conf += m.estimated_close_confidence;
    total_rep  += m.rep_adherence_score;
    total_buy  += m.buyer_adherence_score;
    total_mile += m.milestone_progress_score;
    total_qual += m.map_quality_score;
  }

  const n = mockMAPs.length;

  return NextResponse.json({
    maps,
    summary: {
      total: n,
      health_counts,
      pattern_counts,
      signal_counts,
      action_counts,
      avg_map_adherence_composite:  Math.round((total_comp / n) * 10) / 10,
      avg_close_confidence:         Math.round((total_conf / n) * 10) / 10,
      healthy_map_count:            mockMAPs.filter((m) => m.is_healthy_map).length,
      reset_needed_count:           mockMAPs.filter((m) => m.needs_map_reset).length,
      avg_rep_adherence_score:      Math.round((total_rep / n) * 10) / 10,
      avg_buyer_adherence_score:    Math.round((total_buy / n) * 10) / 10,
      avg_milestone_progress_score: Math.round((total_mile / n) * 10) / 10,
      avg_map_quality_score:        Math.round((total_qual / n) * 10) / 10,
    },
  });
}
