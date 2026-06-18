import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    email_sequence_risk: "low", email_sequence_pattern: "none",
    email_sequence_severity: "strong", recommended_action: "no_action",
    engagement_decay_score: 0.0, sequence_quality_score: 0.0,
    timing_optimization_score: 0.0, conversion_effectiveness_score: 0.0,
    email_sequence_composite: 0.0,
    has_sequence_gap: false, requires_sequence_coaching: false,
    estimated_pipeline_impact_usd: 0.0,
    email_sequence_signal: "Email sequence performance healthy — engagement, personalization, and conversion within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    email_sequence_risk: "low", email_sequence_pattern: "none",
    email_sequence_severity: "strong", recommended_action: "no_action",
    engagement_decay_score: 3.0, sequence_quality_score: 5.0,
    timing_optimization_score: 2.0, conversion_effectiveness_score: 4.0,
    email_sequence_composite: 3.5,
    has_sequence_gap: false, requires_sequence_coaching: false,
    estimated_pipeline_impact_usd: 0.0,
    email_sequence_signal: "Email sequence performance healthy — engagement, personalization, and conversion within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    email_sequence_risk: "moderate", email_sequence_pattern: "template_overuse",
    email_sequence_severity: "developing", recommended_action: "sequence_optimization",
    engagement_decay_score: 15.0, sequence_quality_score: 28.0,
    timing_optimization_score: 12.0, conversion_effectiveness_score: 18.0,
    email_sequence_composite: 18.9,
    has_sequence_gap: false, requires_sequence_coaching: false,
    estimated_pipeline_impact_usd: 9720.0,
    email_sequence_signal: "Template overuse — 28% open rate — 9% reply rate — 4.2% email-to-meeting — composite 19",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    email_sequence_risk: "moderate", email_sequence_pattern: "timing_failure",
    email_sequence_severity: "developing", recommended_action: "timing_recalibration",
    engagement_decay_score: 20.0, sequence_quality_score: 18.0,
    timing_optimization_score: 35.0, conversion_effectiveness_score: 15.0,
    email_sequence_composite: 22.75,
    has_sequence_gap: false, requires_sequence_coaching: true,
    estimated_pipeline_impact_usd: 16200.0,
    email_sequence_signal: "Timing failure — 25% open rate — 8% reply rate — 3.5% email-to-meeting — composite 23",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    email_sequence_risk: "high", email_sequence_pattern: "poor_personalization",
    email_sequence_severity: "weak", recommended_action: "personalization_coaching",
    engagement_decay_score: 35.0, sequence_quality_score: 42.0,
    timing_optimization_score: 28.0, conversion_effectiveness_score: 30.0,
    email_sequence_composite: 35.05,
    has_sequence_gap: true, requires_sequence_coaching: true,
    estimated_pipeline_impact_usd: 47040.0,
    email_sequence_signal: "Poor personalization — 18% open rate — 5% reply rate — 2.8% email-to-meeting — composite 35",
  },
  {
    rep_id: "rep_006", region: "West",
    email_sequence_risk: "high", email_sequence_pattern: "low_open_rate",
    email_sequence_severity: "weak", recommended_action: "sequence_optimization",
    engagement_decay_score: 48.0, sequence_quality_score: 35.0,
    timing_optimization_score: 32.0, conversion_effectiveness_score: 40.0,
    email_sequence_composite: 39.8,
    has_sequence_gap: true, requires_sequence_coaching: true,
    estimated_pipeline_impact_usd: 68040.0,
    email_sequence_signal: "Low open rate — 14% open rate — 4% reply rate — 2.1% email-to-meeting — composite 40",
  },
  {
    rep_id: "rep_007", region: "APAC",
    email_sequence_risk: "critical", email_sequence_pattern: "email_fatigue",
    email_sequence_severity: "failing", recommended_action: "email_fatigue_intervention",
    engagement_decay_score: 72.0, sequence_quality_score: 60.0,
    timing_optimization_score: 55.0, conversion_effectiveness_score: 65.0,
    email_sequence_composite: 63.75,
    has_sequence_gap: true, requires_sequence_coaching: true,
    estimated_pipeline_impact_usd: 136080.0,
    email_sequence_signal: "Email fatigue — 10% open rate — 2% reply rate — 1.5% email-to-meeting — composite 64",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    email_sequence_risk: "critical", email_sequence_pattern: "low_open_rate",
    email_sequence_severity: "failing", recommended_action: "sequence_optimization",
    engagement_decay_score: 95.0, sequence_quality_score: 85.0,
    timing_optimization_score: 80.0, conversion_effectiveness_score: 78.0,
    email_sequence_composite: 85.7,
    has_sequence_gap: true, requires_sequence_coaching: true,
    estimated_pipeline_impact_usd: 252000.0,
    email_sequence_signal: "Low open rate — 8% open rate — 1% reply rate — 0.8% email-to-meeting — composite 86",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-email-sequence-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.email_sequence_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.email_sequence_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_eng = 0, total_qual = 0, total_tim = 0, total_conv = 0, total_impact = 0;

  for (const r of mockReps) {
    risk_counts[r.email_sequence_risk]       = (risk_counts[r.email_sequence_risk] || 0) + 1;
    pattern_counts[r.email_sequence_pattern] = (pattern_counts[r.email_sequence_pattern] || 0) + 1;
    severity_counts[r.email_sequence_severity] = (severity_counts[r.email_sequence_severity] || 0) + 1;
    action_counts[r.recommended_action]      = (action_counts[r.recommended_action] || 0) + 1;
    total_comp   += r.email_sequence_composite;
    total_eng    += r.engagement_decay_score;
    total_qual   += r.sequence_quality_score;
    total_tim    += r.timing_optimization_score;
    total_conv   += r.conversion_effectiveness_score;
    total_impact += r.estimated_pipeline_impact_usd;
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
      avg_email_sequence_composite:             Math.round((total_comp / n) * 10) / 10,
      sequence_gap_count:                       mockReps.filter((r) => r.has_sequence_gap).length,
      coaching_count:                           mockReps.filter((r) => r.requires_sequence_coaching).length,
      avg_engagement_decay_score:               Math.round((total_eng / n) * 10) / 10,
      avg_sequence_quality_score:               Math.round((total_qual / n) * 10) / 10,
      avg_timing_optimization_score:            Math.round((total_tim / n) * 10) / 10,
      avg_conversion_effectiveness_score:       Math.round((total_conv / n) * 10) / 10,
      total_estimated_pipeline_impact_usd:      Math.round(total_impact * 100) / 100,
    },
  });
}
