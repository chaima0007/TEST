import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[rep-incentive-misalignment-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", rep_name: "Alice Chen", region: "West",
    misalignment_rating: "aligned", misalignment_risk: "low",
    primary_misalignment_type: "none", incentive_action: "no_action",
    behavior_alignment_score: 100.0, strategic_alignment_score: 95.0,
    discount_discipline_score: 100.0, revenue_quality_score: 92.0,
    misalignment_composite: 2.2, is_gaming_quota: false, requires_plan_review: false,
    estimated_revenue_risk_usd: 6325.0,
    misalignment_signal: "compensation plan well-aligned — rep behavior matches company objectives",
    quota_usd: 1200000.0, closed_won_usd: 1150000.0,
  },
  {
    rep_id: "rep_002", rep_name: "Marcus Hayes", region: "East",
    misalignment_rating: "moderate", misalignment_risk: "high",
    primary_misalignment_type: "sandbagging", incentive_action: "plan_review",
    behavior_alignment_score: 38.0, strategic_alignment_score: 72.0,
    discount_discipline_score: 80.0, revenue_quality_score: 65.0,
    misalignment_composite: 44.7, is_gaming_quota: true, requires_plan_review: true,
    estimated_revenue_risk_usd: 101925.0,
    misalignment_signal: "sandbagging detected — 72% of closes in final 2 weeks, forecast accuracy 42%",
    quota_usd: 900000.0, closed_won_usd: 910000.0,
  },
  {
    rep_id: "rep_003", rep_name: "Sofia Reyes", region: "Central",
    misalignment_rating: "minor", misalignment_risk: "moderate",
    primary_misalignment_type: "account_neglect", incentive_action: "monitor",
    behavior_alignment_score: 78.0, strategic_alignment_score: 48.0,
    discount_discipline_score: 88.0, revenue_quality_score: 74.0,
    misalignment_composite: 27.6, is_gaming_quota: false, requires_plan_review: false,
    estimated_revenue_risk_usd: 24840.0,
    misalignment_signal: "3 renewal neglects — strategic revenue 24% vs 40% target",
    quota_usd: 800000.0, closed_won_usd: 720000.0,
  },
  {
    rep_id: "rep_004", rep_name: "Ryan Blackwell", region: "Southeast",
    misalignment_rating: "severe", misalignment_risk: "high",
    primary_misalignment_type: "discount_abuse", incentive_action: "manager_coaching",
    behavior_alignment_score: 65.0, strategic_alignment_score: 60.0,
    discount_discipline_score: 22.0, revenue_quality_score: 55.0,
    misalignment_composite: 57.0, is_gaming_quota: false, requires_plan_review: true,
    estimated_revenue_risk_usd: 118125.0,
    misalignment_signal: "discounting 14.2pts above company avg — margin erosion risk",
    quota_usd: 750000.0, closed_won_usd: 820000.0,
  },
  {
    rep_id: "rep_005", rep_name: "Priya Nair", region: "Northeast",
    misalignment_rating: "critical", misalignment_risk: "critical",
    primary_misalignment_type: "quota_gaming", incentive_action: "comp_restructure",
    behavior_alignment_score: 18.0, strategic_alignment_score: 40.0,
    discount_discipline_score: 35.0, revenue_quality_score: 42.0,
    misalignment_composite: 73.9, is_gaming_quota: true, requires_plan_review: true,
    estimated_revenue_risk_usd: 152438.0,
    misalignment_signal: "quota gaming pattern — 78% late-quarter closes, 4 commission disputes",
    quota_usd: 1000000.0, closed_won_usd: 825000.0,
  },
  {
    rep_id: "rep_006", rep_name: "Jordan Walsh", region: "Northwest",
    misalignment_rating: "aligned", misalignment_risk: "low",
    primary_misalignment_type: "none", incentive_action: "no_action",
    behavior_alignment_score: 95.0, strategic_alignment_score: 88.0,
    discount_discipline_score: 92.0, revenue_quality_score: 85.0,
    misalignment_composite: 9.5, is_gaming_quota: false, requires_plan_review: false,
    estimated_revenue_risk_usd: 13969.0,
    misalignment_signal: "compensation plan well-aligned — rep behavior matches company objectives",
    quota_usd: 600000.0, closed_won_usd: 590000.0,
  },
  {
    rep_id: "rep_007", rep_name: "Caleb Stone", region: "Southwest",
    misalignment_rating: "moderate", misalignment_risk: "moderate",
    primary_misalignment_type: "cherry_picking", incentive_action: "plan_review",
    behavior_alignment_score: 72.0, strategic_alignment_score: 58.0,
    discount_discipline_score: 70.0, revenue_quality_score: 28.0,
    misalignment_composite: 42.6, is_gaming_quota: false, requires_plan_review: true,
    estimated_revenue_risk_usd: 55380.0,
    misalignment_signal: "avg deal size $32,000 vs company avg $90,000 — cherry-picking small deals",
    quota_usd: 520000.0, closed_won_usd: 520000.0,
  },
  {
    rep_id: "rep_008", rep_name: "Nina Cross", region: "Central",
    misalignment_rating: "minor", misalignment_risk: "moderate",
    primary_misalignment_type: "account_neglect", incentive_action: "monitor",
    behavior_alignment_score: 82.0, strategic_alignment_score: 52.0,
    discount_discipline_score: 85.0, revenue_quality_score: 78.0,
    misalignment_composite: 26.1, is_gaming_quota: false, requires_plan_review: false,
    estimated_revenue_risk_usd: 21094.0,
    misalignment_signal: "minor incentive friction — composite misalignment score 26",
    quota_usd: 680000.0, closed_won_usd: 645000.0,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const rating = searchParams.get("rating");
  const risk   = searchParams.get("risk");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/rep-incentive-misalignment-engine`);
      if (rating) url.searchParams.set("rating", rating);
      if (risk)   url.searchParams.set("risk",   risk);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let reps = [...mockReps];
  if (rating) reps = reps.filter((r) => r.misalignment_rating === rating);
  if (risk)   reps = reps.filter((r) => r.misalignment_risk   === risk);

  const rating_counts: Record<string, number> = {};
  const risk_counts:   Record<string, number> = {};
  const type_counts:   Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  let total_comp = 0, total_behavior = 0, total_strategic = 0, total_discount = 0, total_quality = 0, total_rev_risk = 0;

  for (const r of mockReps) {
    rating_counts[r.misalignment_rating]         = (rating_counts[r.misalignment_rating] || 0) + 1;
    risk_counts[r.misalignment_risk]             = (risk_counts[r.misalignment_risk] || 0) + 1;
    type_counts[r.primary_misalignment_type]     = (type_counts[r.primary_misalignment_type] || 0) + 1;
    action_counts[r.incentive_action]            = (action_counts[r.incentive_action] || 0) + 1;
    total_comp      += r.misalignment_composite;
    total_behavior  += r.behavior_alignment_score;
    total_strategic += r.strategic_alignment_score;
    total_discount  += r.discount_discipline_score;
    total_quality   += r.revenue_quality_score;
    total_rev_risk  += r.estimated_revenue_risk_usd;
  }

  const n = mockReps.length;

  return sealResponse(NextResponse.json({
    reps,
    summary: {
      total:                         n,
      rating_counts,
      risk_counts,
      type_counts,
      action_counts,
      avg_misalignment_composite:    Math.round((total_comp      / n) * 10) / 10,
      gaming_quota_count:            mockReps.filter((r) => r.is_gaming_quota).length,
      plan_review_count:             mockReps.filter((r) => r.requires_plan_review).length,
      avg_behavior_alignment_score:  Math.round((total_behavior  / n) * 10) / 10,
      avg_strategic_alignment_score: Math.round((total_strategic / n) * 10) / 10,
      avg_discount_discipline_score: Math.round((total_discount  / n) * 10) / 10,
      avg_revenue_quality_score:     Math.round((total_quality   / n) * 10) / 10,
      total_revenue_risk_usd:        Math.round(total_rev_risk),
    },
  }));
}
