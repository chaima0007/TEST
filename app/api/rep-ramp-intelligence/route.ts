import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", rep_name: "Alice Martin", region: "NAMER",
    ramp_status: "on_track", ramp_phase: "ramping", ramp_risk: "low",
    ramp_action: "maintain",
    activity_score: 92.0, readiness_score: 88.0,
    pipeline_health_score: 85.0, attainment_score: 80.0,
    ramp_composite: 86.3, projected_full_ramp_days: 153,
    is_on_track: true, needs_intervention: false,
    key_risk_factor: "none",
    hire_date_days_ago: 60, expected_ramp_days: 180,
    revenue_attainment_pct: 22.0,
  },
  {
    rep_id: "rep_002", rep_name: "Bruno Silva", region: "EMEA",
    ramp_status: "behind", ramp_phase: "learning", ramp_risk: "critical",
    ramp_action: "performance_improvement_plan",
    activity_score: 18.0, readiness_score: 22.0,
    pipeline_health_score: 12.0, attainment_score: 8.0,
    ramp_composite: 15.0, projected_full_ramp_days: 288,
    is_on_track: false, needs_intervention: true,
    key_risk_factor: "product certification incomplete",
    hire_date_days_ago: 75, expected_ramp_days: 180,
    revenue_attainment_pct: 2.0,
  },
  {
    rep_id: "rep_003", rep_name: "Clara Nguyen", region: "APAC",
    ramp_status: "ahead", ramp_phase: "approaching_quota", ramp_risk: "low",
    ramp_action: "maintain",
    activity_score: 98.0, readiness_score: 95.0,
    pipeline_health_score: 97.0, attainment_score: 94.0,
    ramp_composite: 95.8, projected_full_ramp_days: 130,
    is_on_track: true, needs_intervention: false,
    key_risk_factor: "none",
    hire_date_days_ago: 90, expected_ramp_days: 180,
    revenue_attainment_pct: 55.0,
  },
  {
    rep_id: "rep_004", rep_name: "Diego Ferreira", region: "LATAM",
    ramp_status: "at_risk", ramp_phase: "ramping", ramp_risk: "high",
    ramp_action: "accelerate_coaching",
    activity_score: 42.0, readiness_score: 38.0,
    pipeline_health_score: 35.0, attainment_score: 22.0,
    ramp_composite: 35.3, projected_full_ramp_days: 252,
    is_on_track: false, needs_intervention: true,
    key_risk_factor: "low revenue attainment",
    hire_date_days_ago: 50, expected_ramp_days: 180,
    revenue_attainment_pct: 5.0,
  },
  {
    rep_id: "rep_005", rep_name: "Elena Kovacs", region: "EMEA",
    ramp_status: "on_track", ramp_phase: "ramping", ramp_risk: "moderate",
    ramp_action: "territory_adjustment",
    activity_score: 65.0, readiness_score: 70.0,
    pipeline_health_score: 58.0, attainment_score: 48.0,
    ramp_composite: 60.5, projected_full_ramp_days: 180,
    is_on_track: true, needs_intervention: false,
    key_risk_factor: "weak pipeline",
    hire_date_days_ago: 45, expected_ramp_days: 180,
    revenue_attainment_pct: 12.0,
  },
  {
    rep_id: "rep_006", rep_name: "Felix Okafor", region: "NAMER",
    ramp_status: "at_risk", ramp_phase: "ramping", ramp_risk: "high",
    ramp_action: "accelerate_coaching",
    activity_score: 38.0, readiness_score: 55.0,
    pipeline_health_score: 40.0, attainment_score: 30.0,
    ramp_composite: 41.0, projected_full_ramp_days: 225,
    is_on_track: false, needs_intervention: false,
    key_risk_factor: "blocked by tooling/admin issues",
    hire_date_days_ago: 30, expected_ramp_days: 180,
    revenue_attainment_pct: 3.0,
  },
  {
    rep_id: "rep_007", rep_name: "Gabriela Torres", region: "LATAM",
    ramp_status: "ahead", ramp_phase: "at_quota", ramp_risk: "low",
    ramp_action: "maintain",
    activity_score: 88.0, readiness_score: 82.0,
    pipeline_health_score: 90.0, attainment_score: 98.0,
    ramp_composite: 89.5, projected_full_ramp_days: 153,
    is_on_track: true, needs_intervention: false,
    key_risk_factor: "none",
    hire_date_days_ago: 150, expected_ramp_days: 180,
    revenue_attainment_pct: 95.0,
  },
  {
    rep_id: "rep_008", rep_name: "Hiro Tanaka", region: "APAC",
    ramp_status: "on_track", ramp_phase: "learning", ramp_risk: "moderate",
    ramp_action: "territory_adjustment",
    activity_score: 55.0, readiness_score: 60.0,
    pipeline_health_score: 48.0, attainment_score: 50.0,
    ramp_composite: 53.3, projected_full_ramp_days: 180,
    is_on_track: false, needs_intervention: false,
    key_risk_factor: "insufficient manager coaching",
    hire_date_days_ago: 20, expected_ramp_days: 180,
    revenue_attainment_pct: 0.0,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const status  = searchParams.get("status");
  const phase   = searchParams.get("phase");
  const region  = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/rep-ramp-intelligence`);
      if (status) url.searchParams.set("status", status);
      if (phase)  url.searchParams.set("phase", phase);
      if (region) url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (status) reps = reps.filter((r) => r.ramp_status === status);
  if (phase)  reps = reps.filter((r) => r.ramp_phase === phase);
  if (region) reps = reps.filter((r) => r.region === region);

  const status_counts:  Record<string, number> = {};
  const phase_counts:   Record<string, number> = {};
  const risk_counts:    Record<string, number> = {};
  const action_counts:  Record<string, number> = {};
  let total_comp = 0, total_act = 0, total_read = 0, total_pipe = 0, total_att = 0;

  for (const r of mockReps) {
    status_counts[r.ramp_status]  = (status_counts[r.ramp_status] || 0) + 1;
    phase_counts[r.ramp_phase]    = (phase_counts[r.ramp_phase] || 0) + 1;
    risk_counts[r.ramp_risk]      = (risk_counts[r.ramp_risk] || 0) + 1;
    action_counts[r.ramp_action]  = (action_counts[r.ramp_action] || 0) + 1;
    total_comp += r.ramp_composite;
    total_act  += r.activity_score;
    total_read += r.readiness_score;
    total_pipe += r.pipeline_health_score;
    total_att  += r.attainment_score;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total: n,
      ramp_status_counts: status_counts,
      ramp_phase_counts: phase_counts,
      ramp_risk_counts: risk_counts,
      action_counts,
      avg_ramp_composite:          Math.round((total_comp / n) * 10) / 10,
      on_track_count:              mockReps.filter((r) => r.is_on_track).length,
      intervention_count:          mockReps.filter((r) => r.needs_intervention).length,
      avg_activity_score:          Math.round((total_act / n) * 10) / 10,
      avg_readiness_score:         Math.round((total_read / n) * 10) / 10,
      avg_pipeline_health_score:   Math.round((total_pipe / n) * 10) / 10,
      avg_attainment_score:        Math.round((total_att / n) * 10) / 10,
      avg_projected_full_ramp_days: Math.round(
        mockReps.reduce((s, r) => s + r.projected_full_ramp_days, 0) / n
      ),
    },
  });
}
