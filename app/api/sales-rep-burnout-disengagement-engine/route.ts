import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sales-rep-burnout-disengagement-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    burnout_risk: "low", burnout_indicator: "none",
    burnout_severity: "stable", recommended_action: "no_action",
    activity_decline_score: 0.0, performance_decay_score: 0.0,
    engagement_score: 0.0, pipeline_health_score: 0.0,
    burnout_composite: 0.0, is_burnout_risk: false, requires_hr_review: false,
    estimated_productivity_loss_pct: 0.0,
    burnout_signal: "Rep engagement and activity within healthy parameters",
  },
  {
    rep_id: "rep_002", region: "East",
    burnout_risk: "low", burnout_indicator: "activity_decline",
    burnout_severity: "stable", recommended_action: "no_action",
    activity_decline_score: 14.0, performance_decay_score: 8.0,
    engagement_score: 5.0, pipeline_health_score: 0.0,
    burnout_composite: 8.5, is_burnout_risk: false, requires_hr_review: false,
    estimated_productivity_loss_pct: 6.4,
    burnout_signal: "Activity down 18% — 16 calls vs 20 prior — composite 9",
  },
  {
    rep_id: "rep_003", region: "Central",
    burnout_risk: "moderate", burnout_indicator: "velocity_slowdown",
    burnout_severity: "watch", recommended_action: "manager_checkin",
    activity_decline_score: 12.0, performance_decay_score: 22.0,
    engagement_score: 18.0, pipeline_health_score: 8.0,
    burnout_composite: 16.2, is_burnout_risk: false, requires_hr_review: false,
    estimated_productivity_loss_pct: 12.2,
    burnout_signal: "Deal cycle grew from 28d to 42d — composite 16",
  },
  {
    rep_id: "rep_004", region: "Southeast",
    burnout_risk: "moderate", burnout_indicator: "quality_degradation",
    burnout_severity: "watch", recommended_action: "manager_checkin",
    activity_decline_score: 18.0, performance_decay_score: 38.0,
    engagement_score: 20.0, pipeline_health_score: 10.0,
    burnout_composite: 22.7, is_burnout_risk: false, requires_hr_review: false,
    estimated_productivity_loss_pct: 17.0,
    burnout_signal: "Attainment dropped 22pts — now 71% — composite 23",
  },
  {
    rep_id: "rep_005", region: "Northeast",
    burnout_risk: "high", burnout_indicator: "activity_decline",
    burnout_severity: "concerning", recommended_action: "hr_review",
    activity_decline_score: 42.0, performance_decay_score: 30.0,
    engagement_score: 28.0, pipeline_health_score: 20.0,
    burnout_composite: 31.7, is_burnout_risk: false, requires_hr_review: true,
    estimated_productivity_loss_pct: 23.8,
    burnout_signal: "Activity down 45% — 11 calls vs 20 prior — composite 32",
  },
  {
    rep_id: "rep_006", region: "Northwest",
    burnout_risk: "high", burnout_indicator: "disengagement",
    burnout_severity: "concerning", recommended_action: "hr_review",
    activity_decline_score: 45.0, performance_decay_score: 35.0,
    engagement_score: 40.0, pipeline_health_score: 35.0,
    burnout_composite: 39.5, is_burnout_risk: false, requires_hr_review: true,
    estimated_productivity_loss_pct: 29.6,
    burnout_signal: "Broad disengagement — calls down 50% — pipeline down 40% — composite 40",
  },
  {
    rep_id: "rep_007", region: "Southwest",
    burnout_risk: "critical", burnout_indicator: "flight_risk",
    burnout_severity: "crisis", recommended_action: "retention_intervention",
    activity_decline_score: 60.0, performance_decay_score: 55.0,
    engagement_score: 65.0, pipeline_health_score: 55.0,
    burnout_composite: 59.5, is_burnout_risk: true, requires_hr_review: true,
    estimated_productivity_loss_pct: 44.6,
    burnout_signal: "4 escalations — peer collaboration 28/100 — composite 60",
  },
  {
    rep_id: "rep_008", region: "Mountain",
    burnout_risk: "critical", burnout_indicator: "disengagement",
    burnout_severity: "crisis", recommended_action: "retention_intervention",
    activity_decline_score: 85.0, performance_decay_score: 70.0,
    engagement_score: 60.0, pipeline_health_score: 100.0,
    burnout_composite: 77.5, is_burnout_risk: true, requires_hr_review: true,
    estimated_productivity_loss_pct: 58.1,
    burnout_signal: "Broad disengagement — calls down 90% — pipeline down 100% — composite 78",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk      = searchParams.get("risk");
  const indicator = searchParams.get("indicator");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-rep-burnout-disengagement-engine`);
      if (risk)      url.searchParams.set("risk", risk);
      if (indicator) url.searchParams.set("indicator", indicator);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)      reps = reps.filter((r) => r.burnout_risk      === risk);
  if (indicator) reps = reps.filter((r) => r.burnout_indicator === indicator);

  const risk_counts:      Record<string, number> = {};
  const indicator_counts: Record<string, number> = {};
  const severity_counts:  Record<string, number> = {};
  const action_counts:    Record<string, number> = {};
  let total_comp = 0, total_act = 0, total_perf = 0, total_eng = 0, total_pipe = 0, total_loss = 0;

  for (const r of mockReps) {
    risk_counts[r.burnout_risk]           = (risk_counts[r.burnout_risk] || 0) + 1;
    indicator_counts[r.burnout_indicator] = (indicator_counts[r.burnout_indicator] || 0) + 1;
    severity_counts[r.burnout_severity]   = (severity_counts[r.burnout_severity] || 0) + 1;
    action_counts[r.recommended_action]   = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.burnout_composite;
    total_act  += r.activity_decline_score;
    total_perf += r.performance_decay_score;
    total_eng  += r.engagement_score;
    total_pipe += r.pipeline_health_score;
    total_loss += r.estimated_productivity_loss_pct;
  }

  const n = mockReps.length;

  return sealResponse(NextResponse.json({
    reps,
    summary: {
      total:                               n,
      risk_counts,
      indicator_counts,
      severity_counts,
      action_counts,
      avg_burnout_composite:               Math.round((total_comp / n) * 10) / 10,
      burnout_risk_count:                  mockReps.filter((r) => r.is_burnout_risk).length,
      hr_review_count:                     mockReps.filter((r) => r.requires_hr_review).length,
      avg_activity_decline_score:          Math.round((total_act  / n) * 10) / 10,
      avg_performance_decay_score:         Math.round((total_perf / n) * 10) / 10,
      avg_engagement_score:                Math.round((total_eng  / n) * 10) / 10,
      avg_pipeline_health_score:           Math.round((total_pipe / n) * 10) / 10,
      avg_estimated_productivity_loss_pct: Math.round((total_loss / n) * 10) / 10,
    },
  }));
}
