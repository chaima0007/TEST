import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    conv_risk: "low", conv_pattern: "none",
    conv_severity: "elite", recommended_action: "no_action",
    listening_score: 0.0, questioning_score: 0.0,
    discovery_score: 0.0, closing_effectiveness_score: 0.0,
    conv_composite: 0.0,
    has_conv_gap: false, requires_conv_coaching: false,
    estimated_revenue_impact_usd: 0.0,
    conv_signal: "Conversation quality strong — listening ratio, questioning depth, and closing effectiveness within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    conv_risk: "low", conv_pattern: "none",
    conv_severity: "elite", recommended_action: "no_action",
    listening_score: 4.0, questioning_score: 3.0,
    discovery_score: 5.0, closing_effectiveness_score: 2.0,
    conv_composite: 3.55,
    has_conv_gap: false, requires_conv_coaching: true,
    estimated_revenue_impact_usd: 0.0,
    conv_signal: "Conversation quality strong — listening ratio, questioning depth, and closing effectiveness within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    conv_risk: "moderate", conv_pattern: "close_avoider",
    conv_severity: "proficient", recommended_action: "questioning_coaching",
    listening_score: 20.0, questioning_score: 22.0,
    discovery_score: 18.0, closing_effectiveness_score: 15.0,
    conv_composite: 19.25,
    has_conv_gap: true, requires_conv_coaching: true,
    estimated_revenue_impact_usd: 58000.0,
    conv_signal: "Close avoider — 52% rep talk time — 6.2 questions/call — 32% calls with next step — composite 19",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    conv_risk: "moderate", conv_pattern: "shallow_questioner",
    conv_severity: "proficient", recommended_action: "questioning_coaching",
    listening_score: 22.0, questioning_score: 28.0,
    discovery_score: 18.0, closing_effectiveness_score: 12.0,
    conv_composite: 20.9,
    has_conv_gap: true, requires_conv_coaching: true,
    estimated_revenue_impact_usd: 84000.0,
    conv_signal: "Shallow questioner — 58% rep talk time — 4.5 questions/call — 48% calls with next step — composite 21",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    conv_risk: "high", conv_pattern: "discovery_skipper",
    conv_severity: "developing", recommended_action: "discovery_framework_coaching",
    listening_score: 40.0, questioning_score: 38.0,
    discovery_score: 42.0, closing_effectiveness_score: 35.0,
    conv_composite: 38.85,
    has_conv_gap: true, requires_conv_coaching: true,
    estimated_revenue_impact_usd: 315000.0,
    conv_signal: "Discovery skipper — 65% rep talk time — 3.8 questions/call — 38% calls with next step — composite 39",
  },
  {
    rep_id: "rep_006", region: "West",
    conv_risk: "high", conv_pattern: "feature_dumper",
    conv_severity: "developing", recommended_action: "value_articulation_coaching",
    listening_score: 48.0, questioning_score: 42.0,
    discovery_score: 40.0, closing_effectiveness_score: 50.0,
    conv_composite: 44.9,
    has_conv_gap: true, requires_conv_coaching: true,
    estimated_revenue_impact_usd: 756000.0,
    conv_signal: "Feature dumper — 68% rep talk time — 3.2 questions/call — 28% calls with next step — composite 45",
  },
  {
    rep_id: "rep_007", region: "APAC",
    conv_risk: "critical", conv_pattern: "monologue_seller",
    conv_severity: "ineffective", recommended_action: "listening_coaching",
    listening_score: 72.0, questioning_score: 65.0,
    discovery_score: 68.0, closing_effectiveness_score: 70.0,
    conv_composite: 69.0,
    has_conv_gap: true, requires_conv_coaching: true,
    estimated_revenue_impact_usd: 1980000.0,
    conv_signal: "Monologue seller — 75% rep talk time — 2.1 questions/call — 18% calls with next step — composite 69",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    conv_risk: "critical", conv_pattern: "monologue_seller",
    conv_severity: "ineffective", recommended_action: "conversation_reset",
    listening_score: 100.0, questioning_score: 100.0,
    discovery_score: 100.0, closing_effectiveness_score: 100.0,
    conv_composite: 100.0,
    has_conv_gap: true, requires_conv_coaching: true,
    estimated_revenue_impact_usd: 4050000.0,
    conv_signal: "Monologue seller — 82% rep talk time — 1.8 questions/call — 12% calls with next step — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-conversation-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.conv_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.conv_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_ls = 0, total_qs = 0, total_ds = 0, total_cs = 0, total_rev = 0;

  for (const r of mockReps) {
    risk_counts[r.conv_risk]         = (risk_counts[r.conv_risk] || 0) + 1;
    pattern_counts[r.conv_pattern]   = (pattern_counts[r.conv_pattern] || 0) + 1;
    severity_counts[r.conv_severity] = (severity_counts[r.conv_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.conv_composite;
    total_ls   += r.listening_score;
    total_qs   += r.questioning_score;
    total_ds   += r.discovery_score;
    total_cs   += r.closing_effectiveness_score;
    total_rev  += r.estimated_revenue_impact_usd;
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
      avg_conv_composite:                     Math.round((total_comp / n) * 10) / 10,
      conv_gap_count:                         mockReps.filter((r) => r.has_conv_gap).length,
      coaching_count:                         mockReps.filter((r) => r.requires_conv_coaching).length,
      avg_listening_score:                    Math.round((total_ls / n) * 10) / 10,
      avg_questioning_score:                  Math.round((total_qs / n) * 10) / 10,
      avg_discovery_score:                    Math.round((total_ds / n) * 10) / 10,
      avg_closing_effectiveness_score:        Math.round((total_cs / n) * 10) / 10,
      total_estimated_revenue_impact_usd:     Math.round(total_rev * 100) / 100,
    },
  });
}
