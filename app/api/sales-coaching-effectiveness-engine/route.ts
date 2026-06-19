import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    coaching_risk: "low", coaching_pattern: "none",
    coaching_severity: "effective", recommended_action: "no_action",
    coaching_frequency_score: 0.0, coaching_impact_score: 0.0,
    coaching_alignment_score: 0.0, manager_effectiveness_score: 0.0,
    coaching_effectiveness_composite: 0.0, is_coaching_ineffective: false,
    requires_coaching_redesign: false, estimated_revenue_impact_usd: 0.0,
    coaching_signal: "Coaching driving measurable performance improvement",
  },
  {
    rep_id: "rep_002", region: "East",
    coaching_risk: "low", coaching_pattern: "none",
    coaching_severity: "effective", recommended_action: "no_action",
    coaching_frequency_score: 8.0, coaching_impact_score: 0.0,
    coaching_alignment_score: 10.0, manager_effectiveness_score: 10.0,
    coaching_effectiveness_composite: 6.6, is_coaching_ineffective: false,
    requires_coaching_redesign: false, estimated_revenue_impact_usd: 0.0,
    coaching_signal: "Coaching driving measurable performance improvement",
  },
  {
    rep_id: "rep_003", region: "Central",
    coaching_risk: "moderate", coaching_pattern: "insufficient_frequency",
    coaching_severity: "developing", recommended_action: "increase_coaching_frequency",
    coaching_frequency_score: 35.0, coaching_impact_score: 18.0,
    coaching_alignment_score: 10.0, manager_effectiveness_score: 15.0,
    coaching_effectiveness_composite: 20.6, is_coaching_ineffective: false,
    requires_coaching_redesign: false, estimated_revenue_impact_usd: 0.0,
    coaching_signal: "Insufficient frequency — win rate -2pp post-coaching — composite 21",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    coaching_risk: "moderate", coaching_pattern: "topic_misalignment",
    coaching_severity: "developing", recommended_action: "coaching_topic_reset",
    coaching_frequency_score: 20.0, coaching_impact_score: 18.0,
    coaching_alignment_score: 40.0, manager_effectiveness_score: 15.0,
    coaching_effectiveness_composite: 24.5, is_coaching_ineffective: false,
    requires_coaching_redesign: true, estimated_revenue_impact_usd: 0.0,
    coaching_signal: "Topic misalignment — win rate -2pp post-coaching — 45% topic alignment — composite 25",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    coaching_risk: "high", coaching_pattern: "no_behavioral_change",
    coaching_severity: "stalled", recommended_action: "coaching_topic_reset",
    coaching_frequency_score: 35.0, coaching_impact_score: 48.0,
    coaching_alignment_score: 25.0, manager_effectiveness_score: 25.0,
    coaching_effectiveness_composite: 36.0, is_coaching_ineffective: false,
    requires_coaching_redesign: true, estimated_revenue_impact_usd: 8100.0,
    coaching_signal: "No behavioral change — win rate -5pp post-coaching — attainment -8pp post-coaching — 55% topic alignment — composite 43",
  },
  {
    rep_id: "rep_006", region: "West",
    coaching_risk: "high", coaching_pattern: "manager_ineffectiveness",
    coaching_severity: "stalled", recommended_action: "manager_coaching_training",
    coaching_frequency_score: 20.0, coaching_impact_score: 33.0,
    coaching_alignment_score: 40.0, manager_effectiveness_score: 55.0,
    coaching_effectiveness_composite: 37.0, is_coaching_ineffective: false,
    requires_coaching_redesign: true, estimated_revenue_impact_usd: 12000.0,
    coaching_signal: "Manager ineffectiveness — win rate -4pp post-coaching — 2 recidivism incidents — 45% topic alignment — composite 43",
  },
  {
    rep_id: "rep_007", region: "APAC",
    coaching_risk: "critical", coaching_pattern: "manager_ineffectiveness",
    coaching_severity: "regressing", recommended_action: "external_coach_engagement",
    coaching_frequency_score: 50.0, coaching_impact_score: 65.0,
    coaching_alignment_score: 55.0, manager_effectiveness_score: 65.0,
    coaching_effectiveness_composite: 60.5, is_coaching_ineffective: true,
    requires_coaching_redesign: true, estimated_revenue_impact_usd: 32000.0,
    coaching_signal: "Manager ineffectiveness — win rate -8pp post-coaching — attainment -15pp post-coaching — 3 recidivism incidents — 35% topic alignment — composite 65",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    coaching_risk: "critical", coaching_pattern: "coaching_resistance",
    coaching_severity: "regressing", recommended_action: "performance_management",
    coaching_frequency_score: 78.0, coaching_impact_score: 98.0,
    coaching_alignment_score: 65.0, manager_effectiveness_score: 70.0,
    coaching_effectiveness_composite: 80.3, is_coaching_ineffective: true,
    requires_coaching_redesign: true, estimated_revenue_impact_usd: 65000.0,
    coaching_signal: "Coaching resistance — win rate -15pp post-coaching — attainment -25pp post-coaching — 5 recidivism incidents — 25% topic alignment — composite 80",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-coaching-effectiveness-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.coaching_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.coaching_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_freq = 0, total_imp = 0, total_aln = 0, total_mgr = 0, total_rev = 0;

  for (const r of mockReps) {
    risk_counts[r.coaching_risk]           = (risk_counts[r.coaching_risk] || 0) + 1;
    pattern_counts[r.coaching_pattern]     = (pattern_counts[r.coaching_pattern] || 0) + 1;
    severity_counts[r.coaching_severity]   = (severity_counts[r.coaching_severity] || 0) + 1;
    action_counts[r.recommended_action]    = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.coaching_effectiveness_composite;
    total_freq += r.coaching_frequency_score;
    total_imp  += r.coaching_impact_score;
    total_aln  += r.coaching_alignment_score;
    total_mgr  += r.manager_effectiveness_score;
    total_rev  += r.estimated_revenue_impact_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                                n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_coaching_effectiveness_composite: Math.round((total_comp / n) * 10) / 10,
      ineffective_coaching_count:           mockReps.filter((r) => r.is_coaching_ineffective).length,
      coaching_redesign_count:              mockReps.filter((r) => r.requires_coaching_redesign).length,
      avg_coaching_frequency_score:         Math.round((total_freq / n) * 10) / 10,
      avg_coaching_impact_score:            Math.round((total_imp / n) * 10) / 10,
      avg_coaching_alignment_score:         Math.round((total_aln / n) * 10) / 10,
      avg_manager_effectiveness_score:      Math.round((total_mgr / n) * 10) / 10,
      total_estimated_revenue_impact_usd:   Math.round(total_rev * 100) / 100,
    },
  });
}
