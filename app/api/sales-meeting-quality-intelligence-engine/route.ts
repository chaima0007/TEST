import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    meeting_risk: "low", meeting_pattern: "none",
    meeting_severity: "effective", recommended_action: "no_action",
    meeting_preparation_score: 0.0, meeting_outcome_score: 0.0,
    stakeholder_coverage_score: 0.0, meeting_discipline_score: 0.0,
    meeting_quality_composite: 0.0, has_meeting_effectiveness_gap: false,
    requires_coaching_intervention: false, estimated_revenue_at_risk_usd: 0.0,
    meeting_signal: "Meeting quality driving strong deal progression",
  },
  {
    rep_id: "rep_002", region: "East",
    meeting_risk: "low", meeting_pattern: "none",
    meeting_severity: "effective", recommended_action: "no_action",
    meeting_preparation_score: 7.0, meeting_outcome_score: 5.0,
    stakeholder_coverage_score: 8.0, meeting_discipline_score: 5.0,
    meeting_quality_composite: 6.0, has_meeting_effectiveness_gap: false,
    requires_coaching_intervention: false, estimated_revenue_at_risk_usd: 0.0,
    meeting_signal: "Meeting quality driving strong deal progression",
  },
  {
    rep_id: "rep_003", region: "Central",
    meeting_risk: "moderate", meeting_pattern: "poor_preparation",
    meeting_severity: "developing", recommended_action: "meeting_preparation_coaching",
    meeting_preparation_score: 30.0, meeting_outcome_score: 18.0,
    stakeholder_coverage_score: 15.0, meeting_discipline_score: 20.0,
    meeting_quality_composite: 20.0, has_meeting_effectiveness_gap: false,
    requires_coaching_intervention: true, estimated_revenue_at_risk_usd: 9600.0,
    meeting_signal: "Poor preparation — 4 meetings without next step — 3 without 24h follow-up — composite 20",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    meeting_risk: "moderate", meeting_pattern: "wrong_stakeholders",
    meeting_severity: "developing", recommended_action: "meeting_preparation_coaching",
    meeting_preparation_score: 15.0, meeting_outcome_score: 20.0,
    stakeholder_coverage_score: 35.0, meeting_discipline_score: 18.0,
    meeting_quality_composite: 22.0, has_meeting_effectiveness_gap: false,
    requires_coaching_intervention: true, estimated_revenue_at_risk_usd: 14000.0,
    meeting_signal: "Wrong stakeholders — 5 meetings without next step — composite 22",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    meeting_risk: "high", meeting_pattern: "no_deal_advancement",
    meeting_severity: "ineffective", recommended_action: "deal_advancement_review",
    meeting_preparation_score: 25.0, meeting_outcome_score: 45.0,
    stakeholder_coverage_score: 30.0, meeting_discipline_score: 28.0,
    meeting_quality_composite: 33.0, has_meeting_effectiveness_gap: true,
    requires_coaching_intervention: true, estimated_revenue_at_risk_usd: 54000.0,
    meeting_signal: "No deal advancement — 8 meetings without next step — 6 without 24h follow-up — composite 33",
  },
  {
    rep_id: "rep_006", region: "West",
    meeting_risk: "high", meeting_pattern: "poor_follow_through",
    meeting_severity: "ineffective", recommended_action: "deal_advancement_review",
    meeting_preparation_score: 28.0, meeting_outcome_score: 38.0,
    stakeholder_coverage_score: 35.0, meeting_discipline_score: 48.0,
    meeting_quality_composite: 37.0, has_meeting_effectiveness_gap: true,
    requires_coaching_intervention: true, estimated_revenue_at_risk_usd: 72000.0,
    meeting_signal: "Poor follow through — 7 meetings without next step — 9 without 24h follow-up — 4 prospect cancellations — composite 37",
  },
  {
    rep_id: "rep_007", region: "APAC",
    meeting_risk: "critical", meeting_pattern: "no_deal_advancement",
    meeting_severity: "detrimental", recommended_action: "deal_advancement_review",
    meeting_preparation_score: 55.0, meeting_outcome_score: 65.0,
    stakeholder_coverage_score: 58.0, meeting_discipline_score: 55.0,
    meeting_quality_composite: 60.0, has_meeting_effectiveness_gap: true,
    requires_coaching_intervention: true, estimated_revenue_at_risk_usd: 180000.0,
    meeting_signal: "No deal advancement — 12 meetings without next step — 10 without 24h follow-up — 5 prospect cancellations — composite 60",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    meeting_risk: "critical", meeting_pattern: "wrong_stakeholders",
    meeting_severity: "detrimental", recommended_action: "meeting_cadence_reset",
    meeting_preparation_score: 65.0, meeting_outcome_score: 70.0,
    stakeholder_coverage_score: 72.0, meeting_discipline_score: 65.0,
    meeting_quality_composite: 68.0, has_meeting_effectiveness_gap: true,
    requires_coaching_intervention: true, estimated_revenue_at_risk_usd: 280000.0,
    meeting_signal: "Wrong stakeholders — 15 meetings without next step — 12 without 24h follow-up — 7 prospect cancellations — composite 68",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-meeting-quality-intelligence-engine`);
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
  let total_comp = 0, total_prep = 0, total_out = 0, total_stak = 0, total_disc = 0, total_rev = 0;

  for (const r of mockReps) {
    risk_counts[r.meeting_risk]       = (risk_counts[r.meeting_risk] || 0) + 1;
    pattern_counts[r.meeting_pattern] = (pattern_counts[r.meeting_pattern] || 0) + 1;
    severity_counts[r.meeting_severity] = (severity_counts[r.meeting_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.meeting_quality_composite;
    total_prep += r.meeting_preparation_score;
    total_out  += r.meeting_outcome_score;
    total_stak += r.stakeholder_coverage_score;
    total_disc += r.meeting_discipline_score;
    total_rev  += r.estimated_revenue_at_risk_usd;
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
      avg_meeting_quality_composite:        Math.round((total_comp / n) * 10) / 10,
      effectiveness_gap_count:              mockReps.filter((r) => r.has_meeting_effectiveness_gap).length,
      coaching_intervention_count:          mockReps.filter((r) => r.requires_coaching_intervention).length,
      avg_meeting_preparation_score:        Math.round((total_prep / n) * 10) / 10,
      avg_meeting_outcome_score:            Math.round((total_out / n) * 10) / 10,
      avg_stakeholder_coverage_score:       Math.round((total_stak / n) * 10) / 10,
      avg_meeting_discipline_score:         Math.round((total_disc / n) * 10) / 10,
      total_estimated_revenue_at_risk_usd:  Math.round(total_rev * 100) / 100,
    },
  });
}
