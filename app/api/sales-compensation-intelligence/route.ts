import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", rep_name: "Alex Martin", region: "NAMER",
    comp_risk_level: "high", gaming_pattern: "mixed",
    incentive_alignment: "perverse", comp_action: "immediate_review",
    sandbagging_score: 62.5, spiff_dependency_score: 76.5,
    discount_behavior_score: 28.4, attainment_consistency_score: 72.0,
    compensation_efficiency_score: 58.3, estimated_overcompensation: 0,
    quota_accuracy_score: 88.5, is_gaming_comp: true, needs_comp_review: true,
    base_salary: 80000, ote_salary: 160000, quota: 1200000,
    revenue_closed_qtd: 280000, avg_discount_pct: 18.0,
    quota_attainment_q1: 102.0, quota_attainment_q2: 108.0, quota_attainment_q3: 105.0,
  },
  {
    rep_id: "rep_002", rep_name: "Priya Sharma", region: "EMEA",
    comp_risk_level: "critical", gaming_pattern: "spiff_chasing",
    incentive_alignment: "misaligned", comp_action: "immediate_review",
    sandbagging_score: 24.0, spiff_dependency_score: 82.4,
    discount_behavior_score: 44.2, attainment_consistency_score: 41.0,
    compensation_efficiency_score: 44.2, estimated_overcompensation: 18600,
    quota_accuracy_score: 62.0, is_gaming_comp: true, needs_comp_review: true,
    base_salary: 90000, ote_salary: 180000, quota: 1500000,
    revenue_closed_qtd: 198000, avg_discount_pct: 28.0,
    quota_attainment_q1: 78.0, quota_attainment_q2: 142.0, quota_attainment_q3: 65.0,
  },
  {
    rep_id: "rep_003", rep_name: "Marcus Lee", region: "APAC",
    comp_risk_level: "low", gaming_pattern: "clean",
    incentive_alignment: "well_aligned", comp_action: "maintain",
    sandbagging_score: 8.4, spiff_dependency_score: 12.0,
    discount_behavior_score: 14.6, attainment_consistency_score: 89.0,
    compensation_efficiency_score: 84.0, estimated_overcompensation: 0,
    quota_accuracy_score: 96.0, is_gaming_comp: false, needs_comp_review: false,
    base_salary: 75000, ote_salary: 150000, quota: 1000000,
    revenue_closed_qtd: 310000, avg_discount_pct: 8.0,
    quota_attainment_q1: 97.0, quota_attainment_q2: 103.0, quota_attainment_q3: 101.0,
  },
  {
    rep_id: "rep_004", rep_name: "Sophie Durand", region: "EMEA",
    comp_risk_level: "moderate", gaming_pattern: "sandbagging",
    incentive_alignment: "partially_aligned", comp_action: "monitor",
    sandbagging_score: 58.0, spiff_dependency_score: 22.0,
    discount_behavior_score: 18.0, attainment_consistency_score: 74.0,
    compensation_efficiency_score: 70.0, estimated_overcompensation: 0,
    quota_accuracy_score: 84.0, is_gaming_comp: true, needs_comp_review: false,
    base_salary: 85000, ote_salary: 170000, quota: 1400000,
    revenue_closed_qtd: 295000, avg_discount_pct: 12.0,
    quota_attainment_q1: 106.0, quota_attainment_q2: 109.0, quota_attainment_q3: 107.0,
  },
  {
    rep_id: "rep_005", rep_name: "James Okafor", region: "LATAM",
    comp_risk_level: "high", gaming_pattern: "discount_heavy",
    incentive_alignment: "misaligned", comp_action: "restructure",
    sandbagging_score: 18.0, spiff_dependency_score: 28.0,
    discount_behavior_score: 72.4, attainment_consistency_score: 55.0,
    compensation_efficiency_score: 52.0, estimated_overcompensation: 12400,
    quota_accuracy_score: 74.0, is_gaming_comp: true, needs_comp_review: true,
    base_salary: 70000, ote_salary: 140000, quota: 900000,
    revenue_closed_qtd: 182000, avg_discount_pct: 42.0,
    quota_attainment_q1: 84.0, quota_attainment_q2: 96.0, quota_attainment_q3: 88.0,
  },
  {
    rep_id: "rep_006", rep_name: "Elena Kovacs", region: "EMEA",
    comp_risk_level: "low", gaming_pattern: "clean",
    incentive_alignment: "well_aligned", comp_action: "maintain",
    sandbagging_score: 5.0, spiff_dependency_score: 18.0,
    discount_behavior_score: 10.0, attainment_consistency_score: 92.0,
    compensation_efficiency_score: 91.0, estimated_overcompensation: 0,
    quota_accuracy_score: 94.0, is_gaming_comp: false, needs_comp_review: false,
    base_salary: 88000, ote_salary: 176000, quota: 1300000,
    revenue_closed_qtd: 398000, avg_discount_pct: 6.0,
    quota_attainment_q1: 118.0, quota_attainment_q2: 112.0, quota_attainment_q3: 115.0,
  },
  {
    rep_id: "rep_007", rep_name: "Tyler Wong", region: "NAMER",
    comp_risk_level: "critical", gaming_pattern: "mixed",
    incentive_alignment: "perverse", comp_action: "immediate_review",
    sandbagging_score: 71.0, spiff_dependency_score: 68.0,
    discount_behavior_score: 58.0, attainment_consistency_score: 48.0,
    compensation_efficiency_score: 26.0, estimated_overcompensation: 34200,
    quota_accuracy_score: 58.0, is_gaming_comp: true, needs_comp_review: true,
    base_salary: 95000, ote_salary: 190000, quota: 1600000,
    revenue_closed_qtd: 124000, avg_discount_pct: 34.0,
    quota_attainment_q1: 54.0, quota_attainment_q2: 148.0, quota_attainment_q3: 62.0,
  },
  {
    rep_id: "rep_008", rep_name: "Amara Diallo", region: "APAC",
    comp_risk_level: "moderate", gaming_pattern: "clean",
    incentive_alignment: "partially_aligned", comp_action: "monitor",
    sandbagging_score: 14.0, spiff_dependency_score: 36.0,
    discount_behavior_score: 22.0, attainment_consistency_score: 68.0,
    compensation_efficiency_score: 62.0, estimated_overcompensation: 0,
    quota_accuracy_score: 80.0, is_gaming_comp: false, needs_comp_review: true,
    base_salary: 72000, ote_salary: 144000, quota: 1100000,
    revenue_closed_qtd: 220000, avg_discount_pct: 16.0,
    quota_attainment_q1: 88.0, quota_attainment_q2: 72.0, quota_attainment_q3: 94.0,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk      = searchParams.get("risk");
  const pattern   = searchParams.get("pattern");
  const region    = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-compensation-intelligence`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      if (region)  url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.comp_risk_level === risk);
  if (pattern) reps = reps.filter((r) => r.gaming_pattern === pattern);
  if (region)  reps = reps.filter((r) => r.region === region);

  const risk_counts:      Record<string, number> = {};
  const pattern_counts:   Record<string, number> = {};
  const alignment_counts: Record<string, number> = {};
  const action_counts:    Record<string, number> = {};
  let total_eff = 0, total_sand = 0, total_spiff = 0, total_disc = 0,
      total_quot = 0, total_overcomp = 0;

  for (const r of mockReps) {
    risk_counts[r.comp_risk_level]      = (risk_counts[r.comp_risk_level] || 0) + 1;
    pattern_counts[r.gaming_pattern]    = (pattern_counts[r.gaming_pattern] || 0) + 1;
    alignment_counts[r.incentive_alignment] = (alignment_counts[r.incentive_alignment] || 0) + 1;
    action_counts[r.comp_action]        = (action_counts[r.comp_action] || 0) + 1;
    total_eff      += r.compensation_efficiency_score;
    total_sand     += r.sandbagging_score;
    total_spiff    += r.spiff_dependency_score;
    total_disc     += r.discount_behavior_score;
    total_quot     += r.quota_accuracy_score;
    total_overcomp += r.estimated_overcompensation;
  }

  const n = mockReps.length;

  return NextResponse.json(sealResponse({
    reps,
    summary: {
      total: n,
      risk_counts,
      pattern_counts,
      alignment_counts,
      action_counts,
      avg_compensation_efficiency_score: Math.round((total_eff / n) * 10) / 10,
      avg_sandbagging_score:             Math.round((total_sand / n) * 10) / 10,
      total_estimated_overcompensation:  Math.round(total_overcomp),
      gaming_count:                      mockReps.filter((r) => r.is_gaming_comp).length,
      review_needed_count:               mockReps.filter((r) => r.needs_comp_review).length,
      avg_spiff_dependency_score:        Math.round((total_spiff / n) * 10) / 10,
      avg_discount_behavior_score:       Math.round((total_disc / n) * 10) / 10,
      avg_quota_accuracy_score:          Math.round((total_quot / n) * 10) / 10,
    },
  } as Record<string,unknown>));
}
