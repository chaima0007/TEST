import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sales-proposal-conversion-intelligence-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    proposal_risk: "low", proposal_pattern: "none",
    proposal_severity: "healthy", recommended_action: "no_action",
    proposal_win_rate_score: 0.0, proposal_velocity_score: 0.0,
    value_alignment_score: 0.0, competitive_exposure_score: 0.0,
    proposal_effectiveness_composite: 0.0, is_win_rate_declining: false,
    requires_proposal_redesign: false, estimated_lost_revenue_usd: 0.0,
    proposal_signal: "Proposal conversion rate within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    proposal_risk: "low", proposal_pattern: "none",
    proposal_severity: "healthy", recommended_action: "no_action",
    proposal_win_rate_score: 0.0, proposal_velocity_score: 8.0,
    value_alignment_score: 10.0, competitive_exposure_score: 8.0,
    proposal_effectiveness_composite: 7.0, is_win_rate_declining: false,
    requires_proposal_redesign: false, estimated_lost_revenue_usd: 0.0,
    proposal_signal: "Proposal conversion rate within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    proposal_risk: "moderate", proposal_pattern: "proposal_staleness",
    proposal_severity: "declining", recommended_action: "proposal_coaching",
    proposal_win_rate_score: 18.0, proposal_velocity_score: 38.0,
    value_alignment_score: 10.0, competitive_exposure_score: 8.0,
    proposal_effectiveness_composite: 20.0, is_win_rate_declining: false,
    requires_proposal_redesign: false, estimated_lost_revenue_usd: 0.0,
    proposal_signal: "Proposal staleness — 2 stale proposals — composite 20",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    proposal_risk: "moderate", proposal_pattern: "value_misalignment",
    proposal_severity: "declining", recommended_action: "proposal_coaching",
    proposal_win_rate_score: 25.0, proposal_velocity_score: 8.0,
    value_alignment_score: 45.0, competitive_exposure_score: 10.0,
    proposal_effectiveness_composite: 24.0, is_win_rate_declining: false,
    requires_proposal_redesign: true, estimated_lost_revenue_usd: 0.0,
    proposal_signal: "Value misalignment — 40% value alignment — composite 24",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    proposal_risk: "high", proposal_pattern: "poor_win_rate",
    proposal_severity: "stalled", recommended_action: "proposal_coaching",
    proposal_win_rate_score: 55.0, proposal_velocity_score: 20.0,
    value_alignment_score: 25.0, competitive_exposure_score: 18.0,
    proposal_effectiveness_composite: 32.0, is_win_rate_declining: true,
    requires_proposal_redesign: true, estimated_lost_revenue_usd: 11200.0,
    proposal_signal: "Poor win rate — 20% win rate — composite 40",
  },
  {
    rep_id: "rep_006", region: "West",
    proposal_risk: "high", proposal_pattern: "competitive_loss",
    proposal_severity: "stalled", recommended_action: "competitive_repositioning",
    proposal_win_rate_score: 25.0, proposal_velocity_score: 20.0,
    value_alignment_score: 25.0, competitive_exposure_score: 55.0,
    proposal_effectiveness_composite: 33.5, is_win_rate_declining: false,
    requires_proposal_redesign: true, estimated_lost_revenue_usd: 15000.0,
    proposal_signal: "Competitive loss — 3 lost to competition — composite 42",
  },
  {
    rep_id: "rep_007", region: "APAC",
    proposal_risk: "critical", proposal_pattern: "competitive_loss",
    proposal_severity: "critical", recommended_action: "competitive_repositioning",
    proposal_win_rate_score: 55.0, proposal_velocity_score: 55.0,
    value_alignment_score: 55.0, competitive_exposure_score: 65.0,
    proposal_effectiveness_composite: 58.5, is_win_rate_declining: true,
    requires_proposal_redesign: true, estimated_lost_revenue_usd: 48000.0,
    proposal_signal: "Competitive loss — 15% win rate — 3 stale proposals — 35% value alignment — 4 lost to competition — composite 65",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    proposal_risk: "critical", proposal_pattern: "value_misalignment",
    proposal_severity: "critical", recommended_action: "executive_escalation",
    proposal_win_rate_score: 70.0, proposal_velocity_score: 75.0,
    value_alignment_score: 85.0, competitive_exposure_score: 45.0,
    proposal_effectiveness_composite: 72.0, is_win_rate_declining: true,
    requires_proposal_redesign: true, estimated_lost_revenue_usd: 120000.0,
    proposal_signal: "Value misalignment — 10% win rate — 5 stale proposals — 25% value alignment — composite 72",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-proposal-conversion-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.proposal_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.proposal_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_wr = 0, total_vel = 0, total_val = 0, total_ce = 0, total_rev = 0;

  for (const r of mockReps) {
    risk_counts[r.proposal_risk]         = (risk_counts[r.proposal_risk] || 0) + 1;
    pattern_counts[r.proposal_pattern]   = (pattern_counts[r.proposal_pattern] || 0) + 1;
    severity_counts[r.proposal_severity] = (severity_counts[r.proposal_severity] || 0) + 1;
    action_counts[r.recommended_action]  = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.proposal_effectiveness_composite;
    total_wr   += r.proposal_win_rate_score;
    total_vel  += r.proposal_velocity_score;
    total_val  += r.value_alignment_score;
    total_ce   += r.competitive_exposure_score;
    total_rev  += r.estimated_lost_revenue_usd;
  }

  const n = mockReps.length;

  return sealResponse(NextResponse.json({
    reps,
    summary: {
      total:                                  n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_proposal_effectiveness_composite:   Math.round((total_comp / n) * 10) / 10,
      declining_win_rate_count:               mockReps.filter((r) => r.is_win_rate_declining).length,
      proposal_redesign_count:                mockReps.filter((r) => r.requires_proposal_redesign).length,
      avg_proposal_win_rate_score:            Math.round((total_wr / n) * 10) / 10,
      avg_proposal_velocity_score:            Math.round((total_vel / n) * 10) / 10,
      avg_value_alignment_score:              Math.round((total_val / n) * 10) / 10,
      avg_competitive_exposure_score:         Math.round((total_ce / n) * 10) / 10,
      total_estimated_lost_revenue_usd:       Math.round(total_rev * 100) / 100,
    },
  }));
}
