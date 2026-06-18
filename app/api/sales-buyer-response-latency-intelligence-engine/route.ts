import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "REP-001", region: "West",
    latency_risk: "low", latency_pattern: "none",
    latency_severity: "responsive", recommended_action: "no_action",
    latency_score: 5.0, engagement_depth_score: 5.0,
    commitment_score: 5.0, process_velocity_score: 5.0,
    latency_composite: 5.0,
    has_latency_gap: false, requires_latency_intervention: false,
    estimated_at_risk_revenue_usd: 0.0,
    latency_signal: "Buyer engagement healthy — response times, meeting attendance, champion engagement, and process velocity within benchmarks",
  },
  {
    rep_id: "REP-002", region: "East",
    latency_risk: "low", latency_pattern: "none",
    latency_severity: "responsive", recommended_action: "no_action",
    latency_score: 8.0, engagement_depth_score: 7.0,
    commitment_score: 6.0, process_velocity_score: 8.0,
    latency_composite: 7.35,
    has_latency_gap: false, requires_latency_intervention: false,
    estimated_at_risk_revenue_usd: 10000.0,
    latency_signal: "Buyer engagement healthy — response times, meeting attendance, champion engagement, and process velocity within benchmarks",
  },
  {
    rep_id: "REP-003", region: "Central",
    latency_risk: "moderate", latency_pattern: "none",
    latency_severity: "cooling", recommended_action: "engagement_monitoring",
    latency_score: 20.0, engagement_depth_score: 18.0,
    commitment_score: 22.0, process_velocity_score: 16.0,
    latency_composite: 19.7,
    has_latency_gap: false, requires_latency_intervention: true,
    estimated_at_risk_revenue_usd: 35000.0,
    latency_signal: "None — 26h avg buyer response — 8% deals ghosted — 10% meeting no-shows — composite 20",
  },
  {
    rep_id: "REP-004", region: "Northeast",
    latency_risk: "moderate", latency_pattern: "process_stalling",
    latency_severity: "cooling", recommended_action: "engagement_monitoring",
    latency_score: 22.0, engagement_depth_score: 20.0,
    commitment_score: 18.0, process_velocity_score: 32.0,
    latency_composite: 22.3,
    has_latency_gap: false, requires_latency_intervention: true,
    estimated_at_risk_revenue_usd: 60000.0,
    latency_signal: "Process stalling — 30h avg buyer response — 12% deals ghosted — 12% meeting no-shows — composite 22",
  },
  {
    rep_id: "REP-005", region: "Southeast",
    latency_risk: "high", latency_pattern: "commitment_fading",
    latency_severity: "disengaging", recommended_action: "re_engagement_coaching",
    latency_score: 35.0, engagement_depth_score: 32.0,
    commitment_score: 48.0, process_velocity_score: 28.0,
    latency_composite: 37.0,
    has_latency_gap: true, requires_latency_intervention: true,
    estimated_at_risk_revenue_usd: 120000.0,
    latency_signal: "Commitment fading — 50h avg buyer response — 22% deals ghosted — 25% meeting no-shows — composite 37",
  },
  {
    rep_id: "REP-006", region: "West",
    latency_risk: "high", latency_pattern: "champion_cooling",
    latency_severity: "disengaging", recommended_action: "champion_replacement_coaching",
    latency_score: 42.0, engagement_depth_score: 45.0,
    commitment_score: 35.0, process_velocity_score: 30.0,
    latency_composite: 39.75,
    has_latency_gap: true, requires_latency_intervention: true,
    estimated_at_risk_revenue_usd: 180000.0,
    latency_signal: "Champion cooling — 55h avg buyer response — 28% deals ghosted — 20% meeting no-shows — composite 40",
  },
  {
    rep_id: "REP-007", region: "APAC",
    latency_risk: "critical", latency_pattern: "executive_avoidance",
    latency_severity: "ghosted", recommended_action: "deal_abandon_escalation",
    latency_score: 68.0, engagement_depth_score: 58.0,
    commitment_score: 62.0, process_velocity_score: 55.0,
    latency_composite: 62.25,
    has_latency_gap: true, requires_latency_intervention: true,
    estimated_at_risk_revenue_usd: 380000.0,
    latency_signal: "Executive avoidance — 80h avg buyer response — 45% deals ghosted — 40% meeting no-shows — composite 62",
  },
  {
    rep_id: "REP-008", region: "EMEA",
    latency_risk: "critical", latency_pattern: "buyer_ghosting",
    latency_severity: "ghosted", recommended_action: "deal_abandon_escalation",
    latency_score: 78.0, engagement_depth_score: 72.0,
    commitment_score: 70.0, process_velocity_score: 65.0,
    latency_composite: 73.25,
    has_latency_gap: true, requires_latency_intervention: true,
    estimated_at_risk_revenue_usd: 700000.0,
    latency_signal: "Buyer ghosting — 100h avg buyer response — 55% deals ghosted — 50% meeting no-shows — composite 73",
  },
];

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/api/sales-buyer-response-latency-intelligence-engine`, { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_l = 0, total_e = 0, total_c = 0, total_p = 0, total_ar = 0;

  for (const r of mockReps) {
    risk_counts[r.latency_risk]       = (risk_counts[r.latency_risk] || 0) + 1;
    pattern_counts[r.latency_pattern] = (pattern_counts[r.latency_pattern] || 0) + 1;
    severity_counts[r.latency_severity] = (severity_counts[r.latency_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.latency_composite;
    total_l    += r.latency_score;
    total_e    += r.engagement_depth_score;
    total_c    += r.commitment_score;
    total_p    += r.process_velocity_score;
    total_ar   += r.estimated_at_risk_revenue_usd;
  }

  const n = mockReps.length;
  return NextResponse.json({
    reps: mockReps,
    summary: {
      total:                                  n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_latency_composite:                  Math.round((total_comp / n) * 10) / 10,
      latency_gap_count:                      mockReps.filter((r) => r.has_latency_gap).length,
      intervention_count:                     mockReps.filter((r) => r.requires_latency_intervention).length,
      avg_latency_score:                      Math.round((total_l / n) * 10) / 10,
      avg_engagement_depth_score:             Math.round((total_e / n) * 10) / 10,
      avg_commitment_score:                   Math.round((total_c / n) * 10) / 10,
      avg_process_velocity_score:             Math.round((total_p / n) * 10) / 10,
      total_estimated_at_risk_revenue_usd:    Math.round(total_ar * 100) / 100,
    },
  });
}
