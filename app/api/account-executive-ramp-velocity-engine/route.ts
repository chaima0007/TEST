import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    ramp_risk: "low", ramp_blocker: "none",
    ramp_severity: "on_track", recommended_action: "no_action",
    pipeline_gap_score: 0.0, conversion_velocity_score: 0.0,
    knowledge_readiness_score: 0.0, activity_quality_score: 0.0,
    ramp_composite: 0.0, is_under_ramping: false, requires_intervention: false,
    estimated_quota_attainment_pct: 95.0,
    ramp_signal: "AE ramp velocity within healthy parameters",
  },
  {
    rep_id: "rep_002", region: "East",
    ramp_risk: "low", ramp_blocker: "activity_shortfall",
    ramp_severity: "on_track", recommended_action: "no_action",
    pipeline_gap_score: 8.0, conversion_velocity_score: 6.0,
    knowledge_readiness_score: 5.0, activity_quality_score: 12.0,
    ramp_composite: 7.5, is_under_ramping: false, requires_intervention: false,
    estimated_quota_attainment_pct: 88.5,
    ramp_signal: "Minor activity shortfall — composite 8",
  },
  {
    rep_id: "rep_003", region: "Central",
    ramp_risk: "moderate", ramp_blocker: "pipeline_deficit",
    ramp_severity: "behind", recommended_action: "targeted_coaching",
    pipeline_gap_score: 32.0, conversion_velocity_score: 18.0,
    knowledge_readiness_score: 10.0, activity_quality_score: 15.0,
    ramp_composite: 21.8, is_under_ramping: false, requires_intervention: false,
    estimated_quota_attainment_pct: 71.6,
    ramp_signal: "Pipeline at 58% of target — 2 deals vs 4 expected — composite 22",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    ramp_risk: "moderate", ramp_blocker: "slow_conversion",
    ramp_severity: "behind", recommended_action: "targeted_coaching",
    pipeline_gap_score: 20.0, conversion_velocity_score: 38.0,
    knowledge_readiness_score: 12.0, activity_quality_score: 18.0,
    ramp_composite: 24.7, is_under_ramping: false, requires_intervention: false,
    estimated_quota_attainment_pct: 68.2,
    ramp_signal: "Demo-to-proposal rate 35% vs 65% benchmark — composite 25",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    ramp_risk: "high", ramp_blocker: "knowledge_gap",
    ramp_severity: "at_risk", recommended_action: "ramp_plan_adjustment",
    pipeline_gap_score: 40.0, conversion_velocity_score: 35.0,
    knowledge_readiness_score: 55.0, activity_quality_score: 30.0,
    ramp_composite: 41.3, is_under_ramping: true, requires_intervention: true,
    estimated_quota_attainment_pct: 54.4,
    ramp_signal: "Training 42% complete — no product cert — CRM quality 45 — composite 41",
  },
  {
    rep_id: "rep_006", region: "West",
    ramp_risk: "high", ramp_blocker: "coaching_gap",
    ramp_severity: "at_risk", recommended_action: "ramp_plan_adjustment",
    pipeline_gap_score: 35.0, conversion_velocity_score: 28.0,
    knowledge_readiness_score: 30.0, activity_quality_score: 50.0,
    ramp_composite: 34.9, is_under_ramping: false, requires_intervention: true,
    estimated_quota_attainment_pct: 57.0,
    ramp_signal: "0 coaching sessions in 75 days tenure — composite 35",
  },
  {
    rep_id: "rep_007", region: "APAC",
    ramp_risk: "critical", ramp_blocker: "pipeline_deficit",
    ramp_severity: "failing", recommended_action: "pip_initiation",
    pipeline_gap_score: 70.0, conversion_velocity_score: 55.0,
    knowledge_readiness_score: 40.0, activity_quality_score: 45.0,
    ramp_composite: 57.8, is_under_ramping: true, requires_intervention: true,
    estimated_quota_attainment_pct: 37.6,
    ramp_signal: "120d tenure — 0 deals closed — pipeline 15% of target — composite 58",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    ramp_risk: "critical", ramp_blocker: "knowledge_gap",
    ramp_severity: "failing", recommended_action: "separation_review",
    pipeline_gap_score: 80.0, conversion_velocity_score: 75.0,
    knowledge_readiness_score: 70.0, activity_quality_score: 65.0,
    ramp_composite: 74.8, is_under_ramping: true, requires_intervention: true,
    estimated_quota_attainment_pct: 17.0,
    ramp_signal: "180d tenure — 1 deal — training 20% — 0 coaching sessions — composite 75",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const blocker = searchParams.get("blocker");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/account-executive-ramp-velocity-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (blocker) url.searchParams.set("blocker", blocker);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.ramp_risk    === risk);
  if (blocker) reps = reps.filter((r) => r.ramp_blocker === blocker);

  const risk_counts:     Record<string, number> = {};
  const blocker_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_pip = 0, total_conv = 0, total_know = 0, total_act = 0, total_quota = 0;

  for (const r of mockReps) {
    risk_counts[r.ramp_risk]       = (risk_counts[r.ramp_risk] || 0) + 1;
    blocker_counts[r.ramp_blocker] = (blocker_counts[r.ramp_blocker] || 0) + 1;
    severity_counts[r.ramp_severity] = (severity_counts[r.ramp_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp  += r.ramp_composite;
    total_pip   += r.pipeline_gap_score;
    total_conv  += r.conversion_velocity_score;
    total_know  += r.knowledge_readiness_score;
    total_act   += r.activity_quality_score;
    total_quota += r.estimated_quota_attainment_pct;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                              n,
      risk_counts,
      blocker_counts,
      severity_counts,
      action_counts,
      avg_ramp_composite:                 Math.round((total_comp  / n) * 10) / 10,
      under_ramping_count:                mockReps.filter((r) => r.is_under_ramping).length,
      intervention_count:                 mockReps.filter((r) => r.requires_intervention).length,
      avg_pipeline_gap_score:             Math.round((total_pip  / n) * 10) / 10,
      avg_conversion_velocity_score:      Math.round((total_conv / n) * 10) / 10,
      avg_knowledge_readiness_score:      Math.round((total_know / n) * 10) / 10,
      avg_activity_quality_score:         Math.round((total_act  / n) * 10) / 10,
      avg_estimated_quota_attainment_pct: Math.round((total_quota / n) * 10) / 10,
    },
  });
}
