import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sales-reference-intelligence-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    reference_risk: "low", reference_pattern: "none",
    reference_severity: "evidence_led", recommended_action: "no_action",
    reference_utilization_score: 0.0, evidence_diversity_score: 0.0,
    reference_timing_score: 0.0, evidence_depth_score: 0.0,
    reference_composite: 0.0,
    has_reference_gap: false, requires_reference_coaching: false,
    estimated_win_rate_impact_usd: 0.0,
    reference_signal: "Reference usage healthy — customer evidence, case studies, and ROI assets deployed within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    reference_risk: "low", reference_pattern: "none",
    reference_severity: "evidence_led", recommended_action: "no_action",
    reference_utilization_score: 5.0, evidence_diversity_score: 3.0,
    reference_timing_score: 4.0, evidence_depth_score: 2.0,
    reference_composite: 3.8,
    has_reference_gap: false, requires_reference_coaching: false,
    estimated_win_rate_impact_usd: 0.0,
    reference_signal: "Reference usage healthy — customer evidence, case studies, and ROI assets deployed within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    reference_risk: "moderate", reference_pattern: "late_stage_evidence_gap",
    reference_severity: "developing", recommended_action: "evidence_library_training",
    reference_utilization_score: 22.0, evidence_diversity_score: 14.0,
    reference_timing_score: 25.0, evidence_depth_score: 12.0,
    reference_composite: 19.05,
    has_reference_gap: false, requires_reference_coaching: true,
    estimated_win_rate_impact_usd: 9600.0,
    reference_signal: "Late stage evidence gap — 42% deals with reference — 35% deals without evidence — 4 unique refs — composite 19",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    reference_risk: "moderate", reference_pattern: "no_case_study_usage",
    reference_severity: "developing", recommended_action: "evidence_library_training",
    reference_utilization_score: 18.0, evidence_diversity_score: 30.0,
    reference_timing_score: 18.0, evidence_depth_score: 25.0,
    reference_composite: 23.2,
    has_reference_gap: false, requires_reference_coaching: true,
    estimated_win_rate_impact_usd: 19200.0,
    reference_signal: "No case study usage — 48% deals with reference — 38% deals without evidence — 3 unique refs — composite 23",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    reference_risk: "high", reference_pattern: "single_reference_overuse",
    reference_severity: "anecdotal", recommended_action: "reference_rotation_coaching",
    reference_utilization_score: 35.0, reference_timing_score: 30.0,
    evidence_diversity_score: 48.0, evidence_depth_score: 28.0,
    reference_composite: 36.2,
    has_reference_gap: false, requires_reference_coaching: true,
    estimated_win_rate_impact_usd: 54000.0,
    reference_signal: "Single reference overuse — 38% deals with reference — 48% deals without evidence — 2 unique refs — composite 36",
  },
  {
    rep_id: "rep_006", region: "West",
    reference_risk: "high", reference_pattern: "reference_fatigue",
    reference_severity: "anecdotal", recommended_action: "reference_rotation_coaching",
    reference_utilization_score: 40.0, evidence_diversity_score: 38.0,
    reference_timing_score: 52.0, evidence_depth_score: 30.0,
    reference_composite: 41.35,
    has_reference_gap: true, requires_reference_coaching: true,
    estimated_win_rate_impact_usd: 88000.0,
    reference_signal: "Reference fatigue — 28% deals with reference — 52% deals without evidence — 2 unique refs — composite 41",
  },
  {
    rep_id: "rep_007", region: "APAC",
    reference_risk: "critical", reference_pattern: "reference_avoidance",
    reference_severity: "blind", recommended_action: "reference_program_onboarding",
    reference_utilization_score: 70.0, evidence_diversity_score: 65.0,
    reference_timing_score: 60.0, evidence_depth_score: 55.0,
    reference_composite: 64.5,
    has_reference_gap: true, requires_reference_coaching: true,
    estimated_win_rate_impact_usd: 196000.0,
    reference_signal: "Reference avoidance — 12% deals with reference — 68% deals without evidence — 1 unique refs — composite 65",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    reference_risk: "critical", reference_pattern: "reference_avoidance",
    reference_severity: "blind", recommended_action: "reference_program_onboarding",
    reference_utilization_score: 100.0, evidence_diversity_score: 100.0,
    reference_timing_score: 100.0, evidence_depth_score: 100.0,
    reference_composite: 100.0,
    has_reference_gap: true, requires_reference_coaching: true,
    estimated_win_rate_impact_usd: 400000.0,
    reference_signal: "Reference avoidance — 5% deals with reference — 80% deals without evidence — 1 unique refs — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-reference-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.reference_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.reference_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_uti = 0, total_div = 0, total_tim = 0, total_dep = 0, total_impact = 0;

  for (const r of mockReps) {
    risk_counts[r.reference_risk]       = (risk_counts[r.reference_risk] || 0) + 1;
    pattern_counts[r.reference_pattern] = (pattern_counts[r.reference_pattern] || 0) + 1;
    severity_counts[r.reference_severity] = (severity_counts[r.reference_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp   += r.reference_composite;
    total_uti    += r.reference_utilization_score;
    total_div    += r.evidence_diversity_score;
    total_tim    += r.reference_timing_score;
    total_dep    += r.evidence_depth_score;
    total_impact += r.estimated_win_rate_impact_usd;
  }

  const n = mockReps.length;

  return sealResponse(NextResponse.json({
    reps,
    summary: {
      total:                                    n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_reference_composite:                  Math.round((total_comp / n) * 10) / 10,
      reference_gap_count:                      mockReps.filter((r) => r.has_reference_gap).length,
      coaching_count:                           mockReps.filter((r) => r.requires_reference_coaching).length,
      avg_reference_utilization_score:          Math.round((total_uti / n) * 10) / 10,
      avg_evidence_diversity_score:             Math.round((total_div / n) * 10) / 10,
      avg_reference_timing_score:               Math.round((total_tim / n) * 10) / 10,
      avg_evidence_depth_score:                 Math.round((total_dep / n) * 10) / 10,
      total_estimated_win_rate_impact_usd:      Math.round(total_impact * 100) / 100,
    },
  }));
}
