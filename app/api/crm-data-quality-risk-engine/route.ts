import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    data_quality_risk: "low", quality_failure_mode: "none",
    quality_severity: "clean", recommended_action: "no_action",
    completeness_score: 2.0, accuracy_score: 0.0,
    timeliness_score: 3.0, activity_coverage_score: 4.0,
    quality_composite: 2.2, is_data_quality_risk: false, requires_data_audit: false,
    estimated_pipeline_distortion_pct: 1.8,
    quality_signal: "CRM data quality within acceptable parameters",
  },
  {
    rep_id: "rep_002", region: "East",
    data_quality_risk: "moderate", quality_failure_mode: "activity_gap",
    quality_severity: "degraded", recommended_action: "self_remediate",
    completeness_score: 18.0, accuracy_score: 5.0,
    timeliness_score: 10.0, activity_coverage_score: 25.0,
    quality_composite: 14.4, is_data_quality_risk: false, requires_data_audit: false,
    estimated_pipeline_distortion_pct: 11.5,
    quality_signal: "62% records with notes — 2 forecast deals without activity — composite 14",
  },
  {
    rep_id: "rep_003", region: "Central",
    data_quality_risk: "moderate", quality_failure_mode: "missing_data",
    quality_severity: "degraded", recommended_action: "crm_coaching",
    completeness_score: 35.0, accuracy_score: 15.0,
    timeliness_score: 18.0, activity_coverage_score: 20.0,
    quality_composite: 22.7, is_data_quality_risk: false, requires_data_audit: false,
    estimated_pipeline_distortion_pct: 18.2,
    quality_signal: "5 records missing close date — completeness 63% — composite 23",
  },
  {
    rep_id: "rep_004", region: "Southeast",
    data_quality_risk: "high", quality_failure_mode: "stale_records",
    quality_severity: "unreliable", recommended_action: "crm_coaching",
    completeness_score: 28.0, accuracy_score: 20.0,
    timeliness_score: 45.0, activity_coverage_score: 30.0,
    quality_composite: 31.0, is_data_quality_risk: false, requires_data_audit: true,
    estimated_pipeline_distortion_pct: 24.8,
    quality_signal: "8 stale records — avg staleness 42 days — composite 31",
  },
  {
    rep_id: "rep_005", region: "Northeast",
    data_quality_risk: "high", quality_failure_mode: "duplicate_accounts",
    quality_severity: "unreliable", recommended_action: "data_audit",
    completeness_score: 25.0, accuracy_score: 48.0,
    timeliness_score: 25.0, activity_coverage_score: 22.0,
    quality_composite: 30.8, is_data_quality_risk: false, requires_data_audit: true,
    estimated_pipeline_distortion_pct: 24.6,
    quality_signal: "3 duplicate account(s) detected — composite 31",
  },
  {
    rep_id: "rep_006", region: "Northwest",
    data_quality_risk: "high", quality_failure_mode: "stage_drift",
    quality_severity: "unreliable", recommended_action: "data_audit",
    completeness_score: 30.0, accuracy_score: 55.0,
    timeliness_score: 30.0, activity_coverage_score: 35.0,
    quality_composite: 37.3, is_data_quality_risk: false, requires_data_audit: true,
    estimated_pipeline_distortion_pct: 29.8,
    quality_signal: "6 stage mismatch(es) — pipeline age vs stage inconsistency — composite 37",
  },
  {
    rep_id: "rep_007", region: "Southwest",
    data_quality_risk: "critical", quality_failure_mode: "missing_data",
    quality_severity: "corrupt", recommended_action: "pipeline_freeze",
    completeness_score: 85.0, accuracy_score: 55.0,
    timeliness_score: 60.0, activity_coverage_score: 65.0,
    quality_composite: 67.0, is_data_quality_risk: true, requires_data_audit: true,
    estimated_pipeline_distortion_pct: 53.6,
    quality_signal: "12 records missing close date — completeness 38% — composite 67",
  },
  {
    rep_id: "rep_008", region: "Mountain",
    data_quality_risk: "critical", quality_failure_mode: "stale_records",
    quality_severity: "corrupt", recommended_action: "pipeline_freeze",
    completeness_score: 50.0, accuracy_score: 65.0,
    timeliness_score: 80.0, activity_coverage_score: 70.0,
    quality_composite: 65.3, is_data_quality_risk: true, requires_data_audit: true,
    estimated_pipeline_distortion_pct: 52.2,
    quality_signal: "15 stale records — avg staleness 78 days — composite 65",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk = searchParams.get("risk");
  const mode = searchParams.get("mode");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/crm-data-quality-risk-engine`);
      if (risk) url.searchParams.set("risk", risk);
      if (mode) url.searchParams.set("mode", mode);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk) reps = reps.filter((r) => r.data_quality_risk    === risk);
  if (mode) reps = reps.filter((r) => r.quality_failure_mode === mode);

  const risk_counts:          Record<string, number> = {};
  const failure_mode_counts:  Record<string, number> = {};
  const severity_counts:      Record<string, number> = {};
  const action_counts:        Record<string, number> = {};
  let total_comp = 0, total_compl = 0, total_acc = 0, total_time = 0, total_act = 0, total_dist = 0;

  for (const r of mockReps) {
    risk_counts[r.data_quality_risk]       = (risk_counts[r.data_quality_risk] || 0) + 1;
    failure_mode_counts[r.quality_failure_mode] = (failure_mode_counts[r.quality_failure_mode] || 0) + 1;
    severity_counts[r.quality_severity]    = (severity_counts[r.quality_severity] || 0) + 1;
    action_counts[r.recommended_action]    = (action_counts[r.recommended_action] || 0) + 1;
    total_comp  += r.quality_composite;
    total_compl += r.completeness_score;
    total_acc   += r.accuracy_score;
    total_time  += r.timeliness_score;
    total_act   += r.activity_coverage_score;
    total_dist  += r.estimated_pipeline_distortion_pct;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                                 n,
      risk_counts,
      failure_mode_counts,
      severity_counts,
      action_counts,
      avg_quality_composite:                 Math.round((total_comp  / n) * 10) / 10,
      data_quality_risk_count:               mockReps.filter((r) => r.is_data_quality_risk).length,
      audit_required_count:                  mockReps.filter((r) => r.requires_data_audit).length,
      avg_completeness_score:                Math.round((total_compl / n) * 10) / 10,
      avg_accuracy_score:                    Math.round((total_acc   / n) * 10) / 10,
      avg_timeliness_score:                  Math.round((total_time  / n) * 10) / 10,
      avg_activity_coverage_score:           Math.round((total_act   / n) * 10) / 10,
      avg_estimated_pipeline_distortion_pct: Math.round((total_dist  / n) * 10) / 10,
    },
  });
}
