import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    channel_risk: "low", channel_pattern: "none",
    channel_severity: "optimized", recommended_action: "no_action",
    channel_diversity_score: 0.0, channel_effectiveness_score: 0.0,
    touch_frequency_score: 0.0, sequence_compliance_score: 0.0,
    channel_engagement_composite: 0.0,
    has_channel_gap: false, requires_channel_coaching: false,
    estimated_pipeline_impact_usd: 0.0,
    channel_signal: "Multi-channel outreach balanced and performing within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    channel_risk: "low", channel_pattern: "none",
    channel_severity: "optimized", recommended_action: "no_action",
    channel_diversity_score: 3.0, channel_effectiveness_score: 4.0,
    touch_frequency_score: 5.0, sequence_compliance_score: 3.0,
    channel_engagement_composite: 3.8,
    has_channel_gap: false, requires_channel_coaching: false,
    estimated_pipeline_impact_usd: 0.0,
    channel_signal: "Multi-channel outreach balanced and performing within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    channel_risk: "moderate", channel_pattern: "digital_only_approach",
    channel_severity: "developing", recommended_action: "channel_coaching",
    channel_diversity_score: 30.0, channel_effectiveness_score: 10.0,
    touch_frequency_score: 12.0, sequence_compliance_score: 18.0,
    channel_engagement_composite: 18.45,
    has_channel_gap: false, requires_channel_coaching: false,
    estimated_pipeline_impact_usd: 18450.0,
    channel_signal: "Digital only approach — 2 channel(s) only — 4.2 avg touches/prospect — composite 18",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    channel_risk: "moderate", channel_pattern: "low_touch_frequency",
    channel_severity: "developing", recommended_action: "channel_coaching",
    channel_diversity_score: 20.0, channel_effectiveness_score: 18.0,
    touch_frequency_score: 38.0, sequence_compliance_score: 14.0,
    channel_engagement_composite: 23.25,
    has_channel_gap: false, requires_channel_coaching: false,
    estimated_pipeline_impact_usd: 23250.0,
    channel_signal: "Low touch frequency — 3 channel(s) only — 2.8 avg touches/prospect — composite 23",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    channel_risk: "high", channel_pattern: "poor_email_quality",
    channel_severity: "limited", recommended_action: "email_quality_review",
    channel_diversity_score: 30.0, channel_effectiveness_score: 40.0,
    touch_frequency_score: 20.0, sequence_compliance_score: 22.0,
    channel_engagement_composite: 29.8,
    has_channel_gap: false, requires_channel_coaching: true,
    estimated_pipeline_impact_usd: 44700.0,
    channel_signal: "Poor email quality — 2 channel(s) only — 3.5 avg touches/prospect — 2.0% email reply rate — composite 30",
  },
  {
    rep_id: "rep_006", region: "West",
    channel_risk: "high", channel_pattern: "single_channel_dependency",
    channel_severity: "limited", recommended_action: "channel_coaching",
    channel_diversity_score: 50.0, channel_effectiveness_score: 28.0,
    touch_frequency_score: 25.0, sequence_compliance_score: 20.0,
    channel_engagement_composite: 32.55,
    has_channel_gap: true, requires_channel_coaching: true,
    estimated_pipeline_impact_usd: 65100.0,
    channel_signal: "Single channel dependency — 1 channel(s) only — 3.2 avg touches/prospect — composite 33",
  },
  {
    rep_id: "rep_007", region: "APAC",
    channel_risk: "critical", channel_pattern: "single_channel_dependency",
    channel_severity: "siloed", recommended_action: "multi_channel_training",
    channel_diversity_score: 80.0, channel_effectiveness_score: 60.0,
    touch_frequency_score: 55.0, sequence_compliance_score: 50.0,
    channel_engagement_composite: 63.25,
    has_channel_gap: true, requires_channel_coaching: true,
    estimated_pipeline_impact_usd: 189750.0,
    channel_signal: "Single channel dependency — 1 channel(s) only — 2.1 avg touches/prospect — 1.5% email reply rate — composite 63",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    channel_risk: "critical", channel_pattern: "channel_sequence_violation",
    channel_severity: "siloed", recommended_action: "outreach_sequence_redesign",
    channel_diversity_score: 65.0, channel_effectiveness_score: 75.0,
    touch_frequency_score: 70.0, sequence_compliance_score: 80.0,
    channel_engagement_composite: 72.25,
    has_channel_gap: true, requires_channel_coaching: true,
    estimated_pipeline_impact_usd: 252000.0,
    channel_signal: "Channel sequence violation — 2 channel(s) only — 1.8 avg touches/prospect — 1.2% email reply rate — composite 72",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-multi-channel-engagement-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.channel_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.channel_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_div = 0, total_eff = 0, total_frq = 0, total_seq = 0, total_imp = 0;

  for (const r of mockReps) {
    risk_counts[r.channel_risk]       = (risk_counts[r.channel_risk] || 0) + 1;
    pattern_counts[r.channel_pattern] = (pattern_counts[r.channel_pattern] || 0) + 1;
    severity_counts[r.channel_severity] = (severity_counts[r.channel_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.channel_engagement_composite;
    total_div  += r.channel_diversity_score;
    total_eff  += r.channel_effectiveness_score;
    total_frq  += r.touch_frequency_score;
    total_seq  += r.sequence_compliance_score;
    total_imp  += r.estimated_pipeline_impact_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                                  n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_channel_engagement_composite:       Math.round((total_comp / n) * 10) / 10,
      channel_gap_count:                      mockReps.filter((r) => r.has_channel_gap).length,
      channel_coaching_count:                 mockReps.filter((r) => r.requires_channel_coaching).length,
      avg_channel_diversity_score:            Math.round((total_div / n) * 10) / 10,
      avg_channel_effectiveness_score:        Math.round((total_eff / n) * 10) / 10,
      avg_touch_frequency_score:              Math.round((total_frq / n) * 10) / 10,
      avg_sequence_compliance_score:          Math.round((total_seq / n) * 10) / 10,
      total_estimated_pipeline_impact_usd:    Math.round(total_imp * 100) / 100,
    },
  });
}
