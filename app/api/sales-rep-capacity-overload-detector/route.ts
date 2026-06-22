import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sales-rep-capacity-overload-detector] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    capacity_risk: "low", capacity_stressor: "none",
    capacity_severity: "optimal", recommended_action: "no_action",
    account_load_score: 0.0, deal_volume_score: 0.0,
    activity_strain_score: 0.0, quality_degradation_score: 0.0,
    capacity_composite: 0.0, is_overloaded: false, requires_immediate_relief: false,
    estimated_neglected_pipeline_pct: 0.0,
    capacity_signal: "Rep workload within healthy capacity parameters",
  },
  {
    rep_id: "rep_002", region: "East",
    capacity_risk: "low", capacity_stressor: "deal_volume_excess",
    capacity_severity: "optimal", recommended_action: "no_action",
    account_load_score: 8.0, deal_volume_score: 15.0,
    activity_strain_score: 6.0, quality_degradation_score: 5.0,
    capacity_composite: 9.2, is_overloaded: false, requires_immediate_relief: false,
    estimated_neglected_pipeline_pct: 8.0,
    capacity_signal: "22 deals vs 18 benchmark — 2 untouched 14d+ — composite 9",
  },
  {
    rep_id: "rep_003", region: "Central",
    capacity_risk: "moderate", capacity_stressor: "account_overload",
    capacity_severity: "stretched", recommended_action: "workload_review",
    account_load_score: 38.0, deal_volume_score: 18.0,
    activity_strain_score: 14.0, quality_degradation_score: 8.0,
    capacity_composite: 22.0, is_overloaded: false, requires_immediate_relief: false,
    estimated_neglected_pipeline_pct: 15.0,
    capacity_signal: "52 accounts vs 35 benchmark — 8 not contacted — composite 22",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    capacity_risk: "moderate", capacity_stressor: "admin_burden",
    capacity_severity: "stretched", recommended_action: "workload_review",
    account_load_score: 12.0, deal_volume_score: 20.0,
    activity_strain_score: 40.0, quality_degradation_score: 15.0,
    capacity_composite: 22.6, is_overloaded: false, requires_immediate_relief: false,
    estimated_neglected_pipeline_pct: 12.0,
    capacity_signal: "Admin 18h/wk — selling 20h/wk — 5 overdue tasks — composite 23",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    capacity_risk: "high", capacity_stressor: "deal_volume_excess",
    capacity_severity: "overloaded", recommended_action: "account_redistribution",
    account_load_score: 25.0, deal_volume_score: 55.0,
    activity_strain_score: 28.0, quality_degradation_score: 20.0,
    capacity_composite: 34.2, is_overloaded: false, requires_immediate_relief: true,
    estimated_neglected_pipeline_pct: 32.0,
    capacity_signal: "38 deals vs 18 benchmark — 12 untouched 14d+ — composite 34",
  },
  {
    rep_id: "rep_006", region: "West",
    capacity_risk: "high", capacity_stressor: "activity_overburn",
    capacity_severity: "overloaded", recommended_action: "account_redistribution",
    account_load_score: 20.0, deal_volume_score: 30.0,
    activity_strain_score: 55.0, quality_degradation_score: 22.0,
    capacity_composite: 33.0, is_overloaded: false, requires_immediate_relief: true,
    estimated_neglected_pipeline_pct: 22.0,
    capacity_signal: "192 activities vs 100 benchmark — 8d PTO missed — composite 33",
  },
  {
    rep_id: "rep_007", region: "APAC",
    capacity_risk: "critical", capacity_stressor: "account_overload",
    capacity_severity: "critical", recommended_action: "hire_support",
    account_load_score: 70.0, deal_volume_score: 55.0,
    activity_strain_score: 40.0, quality_degradation_score: 45.0,
    capacity_composite: 56.3, is_overloaded: true, requires_immediate_relief: true,
    estimated_neglected_pipeline_pct: 45.0,
    capacity_signal: "80 accounts vs 35 benchmark — 20 not contacted — composite 56",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    capacity_risk: "critical", capacity_stressor: "admin_burden",
    capacity_severity: "critical", recommended_action: "immediate_relief",
    account_load_score: 60.0, deal_volume_score: 70.0,
    activity_strain_score: 75.0, quality_degradation_score: 65.0,
    capacity_composite: 68.0, is_overloaded: true, requires_immediate_relief: true,
    estimated_neglected_pipeline_pct: 58.0,
    capacity_signal: "Admin 28h/wk — selling 12h/wk — 15 overdue tasks — composite 68",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk     = searchParams.get("risk");
  const stressor = searchParams.get("stressor");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-rep-capacity-overload-detector`);
      if (risk)     url.searchParams.set("risk", risk);
      if (stressor) url.searchParams.set("stressor", stressor);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)     reps = reps.filter((r) => r.capacity_risk     === risk);
  if (stressor) reps = reps.filter((r) => r.capacity_stressor === stressor);

  const risk_counts:     Record<string, number> = {};
  const stressor_counts: Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_acc = 0, total_deal = 0, total_act = 0, total_qual = 0, total_neg = 0;

  for (const r of mockReps) {
    risk_counts[r.capacity_risk]       = (risk_counts[r.capacity_risk] || 0) + 1;
    stressor_counts[r.capacity_stressor] = (stressor_counts[r.capacity_stressor] || 0) + 1;
    severity_counts[r.capacity_severity] = (severity_counts[r.capacity_severity] || 0) + 1;
    action_counts[r.recommended_action]  = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.capacity_composite;
    total_acc  += r.account_load_score;
    total_deal += r.deal_volume_score;
    total_act  += r.activity_strain_score;
    total_qual += r.quality_degradation_score;
    total_neg  += r.estimated_neglected_pipeline_pct;
  }

  const n = mockReps.length;

  return sealResponse(NextResponse.json({
    reps,
    summary: {
      total:                                  n,
      risk_counts,
      stressor_counts,
      severity_counts,
      action_counts,
      avg_capacity_composite:                 Math.round((total_comp / n) * 10) / 10,
      overloaded_count:                       mockReps.filter((r) => r.is_overloaded).length,
      immediate_relief_count:                 mockReps.filter((r) => r.requires_immediate_relief).length,
      avg_account_load_score:                 Math.round((total_acc  / n) * 10) / 10,
      avg_deal_volume_score:                  Math.round((total_deal / n) * 10) / 10,
      avg_activity_strain_score:              Math.round((total_act  / n) * 10) / 10,
      avg_quality_degradation_score:          Math.round((total_qual / n) * 10) / 10,
      avg_estimated_neglected_pipeline_pct:   Math.round((total_neg  / n) * 10) / 10,
    },
  }));
}
