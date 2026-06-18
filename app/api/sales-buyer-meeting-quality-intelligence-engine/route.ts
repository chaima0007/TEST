import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    meeting_risk: "low", meeting_pattern: "none",
    meeting_severity: "structured", recommended_action: "no_action",
    meeting_prep_score: 0.0, meeting_engagement_score: 0.0,
    meeting_outcome_score: 0.0, meeting_conversion_score: 0.0,
    meeting_composite: 0.0,
    has_meeting_gap: false, requires_meeting_coaching: false,
    estimated_pipeline_drag_usd: 0.0,
    meeting_signal: "Meeting quality healthy — preparation, stakeholder engagement, and next-step discipline within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    meeting_risk: "low", meeting_pattern: "none",
    meeting_severity: "structured", recommended_action: "no_action",
    meeting_prep_score: 4.0, meeting_engagement_score: 3.0,
    meeting_outcome_score: 5.0, meeting_conversion_score: 2.0,
    meeting_composite: 3.55,
    has_meeting_gap: false, requires_meeting_coaching: false,
    estimated_pipeline_drag_usd: 0.0,
    meeting_signal: "Meeting quality healthy — preparation, stakeholder engagement, and next-step discipline within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    meeting_risk: "moderate", meeting_pattern: "poor_followup",
    meeting_severity: "developing", recommended_action: "meeting_prep_coaching",
    meeting_prep_score: 18.0, meeting_engagement_score: 14.0,
    meeting_outcome_score: 22.0, meeting_conversion_score: 28.0,
    meeting_composite: 20.3,
    has_meeting_gap: false, requires_meeting_coaching: true,
    estimated_pipeline_drag_usd: 14400.0,
    meeting_signal: "Poor followup — 55% meetings with agenda — 42% next-step committed — 1.8 avg stakeholders — composite 20",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    meeting_risk: "moderate", meeting_pattern: "single_stakeholder_trap",
    meeting_severity: "developing", recommended_action: "meeting_prep_coaching",
    meeting_prep_score: 22.0, meeting_engagement_score: 32.0,
    meeting_outcome_score: 18.0, meeting_conversion_score: 20.0,
    meeting_composite: 23.5,
    has_meeting_gap: false, requires_meeting_coaching: true,
    estimated_pipeline_drag_usd: 24000.0,
    meeting_signal: "Single stakeholder trap — 48% meetings with agenda — 52% next-step committed — 1.1 avg stakeholders — composite 24",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    meeting_risk: "high", meeting_pattern: "no_next_step_close",
    meeting_severity: "ad_hoc", recommended_action: "meeting_prep_coaching",
    meeting_prep_score: 35.0, meeting_engagement_score: 38.0,
    meeting_outcome_score: 55.0, meeting_conversion_score: 30.0,
    meeting_composite: 40.25,
    has_meeting_gap: true, requires_meeting_coaching: true,
    estimated_pipeline_drag_usd: 80000.0,
    meeting_signal: "No next step close — 35% meetings with agenda — 28% next-step committed — 1.3 avg stakeholders — composite 40",
  },
  {
    rep_id: "rep_006", region: "West",
    meeting_risk: "high", meeting_pattern: "no_agenda_discipline",
    meeting_severity: "ad_hoc", recommended_action: "meeting_prep_coaching",
    meeting_prep_score: 62.0, meeting_engagement_score: 40.0,
    meeting_outcome_score: 38.0, meeting_conversion_score: 35.0,
    meeting_composite: 44.45,
    has_meeting_gap: true, requires_meeting_coaching: true,
    estimated_pipeline_drag_usd: 126000.0,
    meeting_signal: "No agenda discipline — 18% meetings with agenda — 38% next-step committed — 1.2 avg stakeholders — composite 44",
  },
  {
    rep_id: "rep_007", region: "APAC",
    meeting_risk: "critical", meeting_pattern: "meeting_fatigue",
    meeting_severity: "chaotic", recommended_action: "meeting_cadence_optimization",
    meeting_prep_score: 60.0, meeting_engagement_score: 72.0,
    meeting_outcome_score: 65.0, meeting_conversion_score: 58.0,
    meeting_composite: 65.3,
    has_meeting_gap: true, requires_meeting_coaching: true,
    estimated_pipeline_drag_usd: 280000.0,
    meeting_signal: "Meeting fatigue — 12% meetings with agenda — 22% next-step committed — 0.9 avg stakeholders — composite 65",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    meeting_risk: "critical", meeting_pattern: "no_agenda_discipline",
    meeting_severity: "chaotic", recommended_action: "meeting_prep_coaching",
    meeting_prep_score: 100.0, meeting_engagement_score: 100.0,
    meeting_outcome_score: 100.0, meeting_conversion_score: 100.0,
    meeting_composite: 100.0,
    has_meeting_gap: true, requires_meeting_coaching: true,
    estimated_pipeline_drag_usd: 560000.0,
    meeting_signal: "No agenda discipline — 5% meetings with agenda — 10% next-step committed — 0.8 avg stakeholders — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-buyer-meeting-quality-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.meeting_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.meeting_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_pre = 0, total_eng = 0, total_out = 0, total_cvt = 0, total_drag = 0;

  for (const r of mockReps) {
    risk_counts[r.meeting_risk]       = (risk_counts[r.meeting_risk] || 0) + 1;
    pattern_counts[r.meeting_pattern] = (pattern_counts[r.meeting_pattern] || 0) + 1;
    severity_counts[r.meeting_severity] = (severity_counts[r.meeting_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.meeting_composite;
    total_pre  += r.meeting_prep_score;
    total_eng  += r.meeting_engagement_score;
    total_out  += r.meeting_outcome_score;
    total_cvt  += r.meeting_conversion_score;
    total_drag += r.estimated_pipeline_drag_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                                    n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_meeting_composite:                    Math.round((total_comp / n) * 10) / 10,
      meeting_gap_count:                        mockReps.filter((r) => r.has_meeting_gap).length,
      coaching_count:                           mockReps.filter((r) => r.requires_meeting_coaching).length,
      avg_meeting_prep_score:                   Math.round((total_pre / n) * 10) / 10,
      avg_meeting_engagement_score:             Math.round((total_eng / n) * 10) / 10,
      avg_meeting_outcome_score:                Math.round((total_out / n) * 10) / 10,
      avg_meeting_conversion_score:             Math.round((total_cvt / n) * 10) / 10,
      total_estimated_pipeline_drag_usd:        Math.round(total_drag * 100) / 100,
    },
  });
}
