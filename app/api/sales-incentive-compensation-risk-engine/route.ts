import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sales-incentive-compensation-risk-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    comp_risk: "low", comp_pattern: "none",
    comp_severity: "aligned", recommended_action: "no_action",
    timing_manipulation_score: 0.0, discount_behavior_score: 0.0,
    quota_gaming_score: 0.0, strategic_alignment_score: 0.0,
    comp_risk_composite: 0.0, is_comp_misaligned: false, requires_immediate_review: false,
    estimated_margin_impact_pct: 0.0,
    comp_signal: "Incentive comp behavior aligned with company objectives",
  },
  {
    rep_id: "rep_002", region: "East",
    comp_risk: "low", comp_pattern: "quarter_end_dumping",
    comp_severity: "watch", recommended_action: "no_action",
    timing_manipulation_score: 14.0, discount_behavior_score: 5.0,
    quota_gaming_score: 4.0, strategic_alignment_score: 6.0,
    comp_risk_composite: 7.3, is_comp_misaligned: false, requires_immediate_review: false,
    estimated_margin_impact_pct: 0.22,
    comp_signal: "Quarter end dumping — 25% of deals in last week of quarter — composite 7",
  },
  {
    rep_id: "rep_003", region: "Central",
    comp_risk: "moderate", comp_pattern: "discount_abuse",
    comp_severity: "watch", recommended_action: "comp_plan_review",
    timing_manipulation_score: 10.0, discount_behavior_score: 28.0,
    quota_gaming_score: 8.0, strategic_alignment_score: 12.0,
    comp_risk_composite: 15.1, is_comp_misaligned: false, requires_immediate_review: false,
    estimated_margin_impact_pct: 0.91,
    comp_signal: "Discount abuse — 2 deals above discount policy — avg discount 8pp above policy — composite 15",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    comp_risk: "moderate", comp_pattern: "cherry_picking",
    comp_severity: "watch", recommended_action: "comp_plan_review",
    timing_manipulation_score: 8.0, discount_behavior_score: 12.0,
    quota_gaming_score: 10.0, strategic_alignment_score: 32.0,
    comp_risk_composite: 15.4, is_comp_misaligned: false, requires_immediate_review: false,
    estimated_margin_impact_pct: 0.77,
    comp_signal: "Cherry picking — 75% transactional deals — 8% strategic account penetration — composite 15",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    comp_risk: "high", comp_pattern: "quota_ratchet_gaming",
    comp_severity: "misaligned", recommended_action: "quota_recalibration",
    timing_manipulation_score: 20.0, discount_behavior_score: 18.0,
    quota_gaming_score: 45.0, strategic_alignment_score: 20.0,
    comp_risk_composite: 26.3, is_comp_misaligned: false, requires_immediate_review: true,
    estimated_margin_impact_pct: 1.32,
    comp_signal: "Quota ratchet gaming — 145% attainment last period — 3 deals delayed to next period — composite 26",
  },
  {
    rep_id: "rep_006", region: "West",
    comp_risk: "high", comp_pattern: "accelerator_exploitation",
    comp_severity: "misaligned", recommended_action: "deal_desk_escalation",
    timing_manipulation_score: 28.0, discount_behavior_score: 35.0,
    quota_gaming_score: 42.0, strategic_alignment_score: 28.0,
    comp_risk_composite: 33.7, is_comp_misaligned: false, requires_immediate_review: true,
    estimated_margin_impact_pct: 2.53,
    comp_signal: "Accelerator exploitation — 4 deals just above accelerator threshold — 45% last week of quarter — composite 34",
  },
  {
    rep_id: "rep_007", region: "APAC",
    comp_risk: "critical", comp_pattern: "accelerator_exploitation",
    comp_severity: "exploiting", recommended_action: "plan_redesign",
    timing_manipulation_score: 65.0, discount_behavior_score: 62.0,
    quota_gaming_score: 70.0, strategic_alignment_score: 55.0,
    comp_risk_composite: 64.0, is_comp_misaligned: true, requires_immediate_review: true,
    estimated_margin_impact_pct: 5.12,
    comp_signal: "Accelerator exploitation — 6 deals just above threshold — 55% of deals in last week — 7 above discount policy — composite 64",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    comp_risk: "critical", comp_pattern: "discount_abuse",
    comp_severity: "exploiting", recommended_action: "plan_redesign",
    timing_manipulation_score: 70.0, discount_behavior_score: 75.0,
    quota_gaming_score: 65.0, strategic_alignment_score: 65.0,
    comp_risk_composite: 70.3, is_comp_misaligned: true, requires_immediate_review: true,
    estimated_margin_impact_pct: 7.03,
    comp_signal: "Discount abuse — 8 deals above policy — avg discount 18pp above policy — 60% in last week — composite 70",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-incentive-compensation-risk-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.comp_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.comp_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_ti = 0, total_di = 0, total_ga = 0, total_al = 0, total_margin = 0;

  for (const r of mockReps) {
    risk_counts[r.comp_risk]          = (risk_counts[r.comp_risk] || 0) + 1;
    pattern_counts[r.comp_pattern]    = (pattern_counts[r.comp_pattern] || 0) + 1;
    severity_counts[r.comp_severity]  = (severity_counts[r.comp_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp   += r.comp_risk_composite;
    total_ti     += r.timing_manipulation_score;
    total_di     += r.discount_behavior_score;
    total_ga     += r.quota_gaming_score;
    total_al     += r.strategic_alignment_score;
    total_margin += r.estimated_margin_impact_pct;
  }

  const n = mockReps.length;

  return sealResponse(NextResponse.json({
    reps,
    summary: {
      total:                             n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_comp_risk_composite:           Math.round((total_comp / n) * 10) / 10,
      misaligned_count:                  mockReps.filter((r) => r.is_comp_misaligned).length,
      immediate_review_count:            mockReps.filter((r) => r.requires_immediate_review).length,
      avg_timing_manipulation_score:     Math.round((total_ti / n) * 10) / 10,
      avg_discount_behavior_score:       Math.round((total_di / n) * 10) / 10,
      avg_quota_gaming_score:            Math.round((total_ga / n) * 10) / 10,
      avg_strategic_alignment_score:     Math.round((total_al / n) * 10) / 10,
      avg_estimated_margin_impact_pct:   Math.round((total_margin / n) * 100) / 100,
    },
  }));
}
