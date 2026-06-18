import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    quota_gaming_risk: "low", gaming_pattern: "none",
    gaming_severity: "clean", recommended_action: "no_action",
    timing_manipulation_score: 0.0, pipeline_integrity_score: 0.0,
    compensation_gaming_score: 0.0, reporting_distortion_score: 0.0,
    gaming_composite: 0.0, is_gaming_quota: false, requires_comp_audit: false,
    estimated_inflated_pipeline_usd: 0.0,
    gaming_signal: "Quota attainment behavior within normal parameters",
  },
  {
    rep_id: "rep_002", region: "East",
    quota_gaming_risk: "low", gaming_pattern: "pull_forward_abuse",
    gaming_severity: "clean", recommended_action: "manager_review",
    timing_manipulation_score: 18.0, pipeline_integrity_score: 5.0,
    compensation_gaming_score: 5.0, reporting_distortion_score: 3.0,
    gaming_composite: 8.5, is_gaming_quota: false, requires_comp_audit: false,
    estimated_inflated_pipeline_usd: 4250.0,
    gaming_signal: "3 deals pulled from next period — composite 9",
  },
  {
    rep_id: "rep_003", region: "Central",
    quota_gaming_risk: "moderate", gaming_pattern: "pipeline_inflation",
    gaming_severity: "watch", recommended_action: "manager_review",
    timing_manipulation_score: 10.0, pipeline_integrity_score: 35.0,
    compensation_gaming_score: 8.0, reporting_distortion_score: 5.0,
    gaming_composite: 15.5, is_gaming_quota: false, requires_comp_audit: false,
    estimated_inflated_pipeline_usd: 23250.0,
    gaming_signal: "2 fake pipeline flag(s) — coverage 8.0x vs 3.0x avg — composite 16",
  },
  {
    rep_id: "rep_004", region: "Southeast",
    quota_gaming_risk: "moderate", gaming_pattern: "close_date_manipulation",
    gaming_severity: "watch", recommended_action: "manager_review",
    timing_manipulation_score: 40.0, pipeline_integrity_score: 12.0,
    compensation_gaming_score: 10.0, reporting_distortion_score: 8.0,
    gaming_composite: 20.7, is_gaming_quota: false, requires_comp_audit: false,
    estimated_inflated_pipeline_usd: 20700.0,
    gaming_signal: "3.8 avg close date changes — 42% closed in final week — composite 21",
  },
  {
    rep_id: "rep_005", region: "Northeast",
    quota_gaming_risk: "high", gaming_pattern: "quota_anchor_gaming",
    gaming_severity: "suspicious", recommended_action: "comp_plan_audit",
    timing_manipulation_score: 12.0, pipeline_integrity_score: 15.0,
    compensation_gaming_score: 52.0, reporting_distortion_score: 10.0,
    gaming_composite: 24.0, is_gaming_quota: false, requires_comp_audit: true,
    estimated_inflated_pipeline_usd: 60000.0,
    gaming_signal: "Over-attainment 148% this period, 141% prior — composite 24",
  },
  {
    rep_id: "rep_006", region: "Northwest",
    quota_gaming_risk: "high", gaming_pattern: "pipeline_inflation",
    gaming_severity: "suspicious", recommended_action: "comp_plan_audit",
    timing_manipulation_score: 22.0, pipeline_integrity_score: 55.0,
    compensation_gaming_score: 18.0, reporting_distortion_score: 12.0,
    gaming_composite: 27.6, is_gaming_quota: false, requires_comp_audit: true,
    estimated_inflated_pipeline_usd: 110400.0,
    gaming_signal: "5 fake pipeline flag(s) — coverage 9.5x vs 3.0x avg — composite 28",
  },
  {
    rep_id: "rep_007", region: "Southwest",
    quota_gaming_risk: "critical", gaming_pattern: "comp_period_stuffing",
    gaming_severity: "confirmed", recommended_action: "compensation_clawback",
    timing_manipulation_score: 55.0, pipeline_integrity_score: 30.0,
    compensation_gaming_score: 45.0, reporting_distortion_score: 60.0,
    gaming_composite: 47.5, is_gaming_quota: true, requires_comp_audit: true,
    estimated_inflated_pipeline_usd: 237500.0,
    gaming_signal: "4 deals reversed post-close — $125,000 revenue reversed — composite 48",
  },
  {
    rep_id: "rep_008", region: "Mountain",
    quota_gaming_risk: "critical", gaming_pattern: "comp_period_stuffing",
    gaming_severity: "confirmed", recommended_action: "compensation_clawback",
    timing_manipulation_score: 70.0, pipeline_integrity_score: 55.0,
    compensation_gaming_score: 65.0, reporting_distortion_score: 70.0,
    gaming_composite: 65.3, is_gaming_quota: true, requires_comp_audit: true,
    estimated_inflated_pipeline_usd: 457100.0,
    gaming_signal: "7 deals reversed post-close — $320,000 revenue reversed — composite 65",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-quota-gaming-detection-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.quota_gaming_risk === risk);
  if (pattern) reps = reps.filter((r) => r.gaming_pattern   === pattern);

  const risk_counts:    Record<string, number> = {};
  const pattern_counts: Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:  Record<string, number> = {};
  let total_comp = 0, total_tim = 0, total_pipe = 0, total_cmp = 0, total_rep = 0, total_infl = 0;

  for (const r of mockReps) {
    risk_counts[r.quota_gaming_risk]   = (risk_counts[r.quota_gaming_risk] || 0) + 1;
    pattern_counts[r.gaming_pattern]   = (pattern_counts[r.gaming_pattern] || 0) + 1;
    severity_counts[r.gaming_severity] = (severity_counts[r.gaming_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.gaming_composite;
    total_tim  += r.timing_manipulation_score;
    total_pipe += r.pipeline_integrity_score;
    total_cmp  += r.compensation_gaming_score;
    total_rep  += r.reporting_distortion_score;
    total_infl += r.estimated_inflated_pipeline_usd;
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
      avg_gaming_composite:                 Math.round((total_comp / n) * 10) / 10,
      gaming_count:                         mockReps.filter((r) => r.is_gaming_quota).length,
      comp_audit_count:                     mockReps.filter((r) => r.requires_comp_audit).length,
      avg_timing_manipulation_score:        Math.round((total_tim  / n) * 10) / 10,
      avg_pipeline_integrity_score:         Math.round((total_pipe / n) * 10) / 10,
      avg_compensation_gaming_score:        Math.round((total_cmp  / n) * 10) / 10,
      avg_reporting_distortion_score:       Math.round((total_rep  / n) * 10) / 10,
      total_estimated_inflated_pipeline_usd: Math.round(total_infl * 100) / 100,
    },
  });
}
