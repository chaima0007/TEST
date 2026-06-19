import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    handoff_risk: "low", handoff_pattern: "none",
    handoff_severity: "seamless", recommended_action: "no_action",
    context_score: 0.0, expectation_score: 0.0,
    continuity_score: 0.0, timing_score: 0.0,
    handoff_composite: 0.0,
    has_handoff_gap: false, requires_handoff_coaching: false,
    estimated_churn_risk_usd: 0.0,
    handoff_signal: "Customer handoff quality strong — context transfer, expectation alignment, and post-sale continuity within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    handoff_risk: "low", handoff_pattern: "none",
    handoff_severity: "seamless", recommended_action: "no_action",
    context_score: 3.0, expectation_score: 4.0,
    continuity_score: 2.0, timing_score: 5.0,
    handoff_composite: 3.5,
    has_handoff_gap: false, requires_handoff_coaching: false,
    estimated_churn_risk_usd: 0.0,
    handoff_signal: "Customer handoff quality strong — context transfer, expectation alignment, and post-sale continuity within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    handoff_risk: "moderate", handoff_pattern: "none",
    handoff_severity: "adequate", recommended_action: "handoff_process_coaching",
    context_score: 22.0, expectation_score: 20.0,
    continuity_score: 22.0, timing_score: 18.0,
    handoff_composite: 21.2,
    has_handoff_gap: true, requires_handoff_coaching: true,
    estimated_churn_risk_usd: 63600.0,
    handoff_signal: "Handoff risk — 55% provide implementation plan — 72% expectation alignment rate — 55% rep involved in onboarding — composite 21",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    handoff_risk: "moderate", handoff_pattern: "late_handoff_timing",
    handoff_severity: "adequate", recommended_action: "handoff_process_coaching",
    context_score: 28.0, expectation_score: 22.0,
    continuity_score: 25.0, timing_score: 35.0,
    handoff_composite: 27.2,
    has_handoff_gap: true, requires_handoff_coaching: true,
    estimated_churn_risk_usd: 108000.0,
    handoff_signal: "Late handoff timing — 48% provide implementation plan — 68% expectation alignment rate — 50% rep involved in onboarding — composite 27",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    handoff_risk: "high", handoff_pattern: "ghosting_at_handoff",
    handoff_severity: "disruptive", recommended_action: "post_sale_involvement_coaching",
    context_score: 42.0, expectation_score: 38.0,
    continuity_score: 55.0, timing_score: 35.0,
    handoff_composite: 43.7,
    has_handoff_gap: true, requires_handoff_coaching: true,
    estimated_churn_risk_usd: 252000.0,
    handoff_signal: "Ghosting at handoff — 40% provide implementation plan — 58% expectation alignment rate — 28% rep involved in onboarding — composite 44",
  },
  {
    rep_id: "rep_006", region: "West",
    handoff_risk: "high", handoff_pattern: "incomplete_context_transfer",
    handoff_severity: "disruptive", recommended_action: "handoff_process_coaching",
    context_score: 55.0, expectation_score: 45.0,
    continuity_score: 48.0, timing_score: 40.0,
    handoff_composite: 48.8,
    has_handoff_gap: true, requires_handoff_coaching: true,
    estimated_churn_risk_usd: 396000.0,
    handoff_signal: "Incomplete context transfer — 30% provide implementation plan — 55% expectation alignment rate — 35% rep involved in onboarding — composite 49",
  },
  {
    rep_id: "rep_007", region: "APAC",
    handoff_risk: "critical", handoff_pattern: "oversell_setup",
    handoff_severity: "damaging", recommended_action: "expectation_alignment_coaching",
    context_score: 75.0, expectation_score: 72.0,
    continuity_score: 68.0, timing_score: 60.0,
    handoff_composite: 70.8,
    has_handoff_gap: true, requires_handoff_coaching: true,
    estimated_churn_risk_usd: 1125000.0,
    handoff_signal: "Oversell setup — 22% provide implementation plan — 42% expectation alignment rate — 20% rep involved in onboarding — composite 71",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    handoff_risk: "critical", handoff_pattern: "oversell_setup",
    handoff_severity: "damaging", recommended_action: "handoff_reset_intervention",
    context_score: 100.0, expectation_score: 100.0,
    continuity_score: 100.0, timing_score: 100.0,
    handoff_composite: 100.0,
    has_handoff_gap: true, requires_handoff_coaching: true,
    estimated_churn_risk_usd: 2200000.0,
    handoff_signal: "Oversell setup — 20% provide implementation plan — 45% expectation alignment rate — 20% rep involved in onboarding — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-customer-success-handoff-quality-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.handoff_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.handoff_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_ctx = 0, total_exp = 0, total_con = 0, total_tim = 0, total_loss = 0;

  for (const r of mockReps) {
    risk_counts[r.handoff_risk]         = (risk_counts[r.handoff_risk] || 0) + 1;
    pattern_counts[r.handoff_pattern]   = (pattern_counts[r.handoff_pattern] || 0) + 1;
    severity_counts[r.handoff_severity] = (severity_counts[r.handoff_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.handoff_composite;
    total_ctx  += r.context_score;
    total_exp  += r.expectation_score;
    total_con  += r.continuity_score;
    total_tim  += r.timing_score;
    total_loss += r.estimated_churn_risk_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                              n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_handoff_composite:              Math.round((total_comp / n) * 10) / 10,
      handoff_gap_count:                  mockReps.filter((r) => r.has_handoff_gap).length,
      coaching_count:                     mockReps.filter((r) => r.requires_handoff_coaching).length,
      avg_context_score:                  Math.round((total_ctx / n) * 10) / 10,
      avg_expectation_score:              Math.round((total_exp / n) * 10) / 10,
      avg_continuity_score:               Math.round((total_con / n) * 10) / 10,
      avg_timing_score:                   Math.round((total_tim / n) * 10) / 10,
      total_estimated_churn_risk_usd:     Math.round(total_loss * 100) / 100,
    },
  });
}
