import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    intent_risk: "low", intent_pattern: "none",
    intent_severity: "engaged", recommended_action: "no_action",
    engagement_decay_score: 0.0, champion_health_score: 0.0,
    buying_signal_score: 0.0, competitive_threat_score: 0.0,
    buyer_intent_composite: 0.0,
    has_intent_gap: false, requires_re_engagement: false,
    estimated_pipeline_at_risk_usd: 0.0,
    intent_signal: "Buyer intent signals healthy — prospects showing active engagement",
  },
  {
    rep_id: "rep_002", region: "East",
    intent_risk: "low", intent_pattern: "none",
    intent_severity: "engaged", recommended_action: "no_action",
    engagement_decay_score: 3.0, champion_health_score: 5.0,
    buying_signal_score: 4.0, competitive_threat_score: 2.0,
    buyer_intent_composite: 3.8,
    has_intent_gap: false, requires_re_engagement: false,
    estimated_pipeline_at_risk_usd: 0.0,
    intent_signal: "Buyer intent signals healthy — prospects showing active engagement",
  },
  {
    rep_id: "rep_003", region: "Central",
    intent_risk: "moderate", intent_pattern: "intent_cooling",
    intent_severity: "lukewarm", recommended_action: "re_engagement_sequence",
    engagement_decay_score: 22.0, champion_health_score: 14.0,
    buying_signal_score: 18.0, competitive_threat_score: 10.0,
    buyer_intent_composite: 17.2,
    has_intent_gap: false, requires_re_engagement: false,
    estimated_pipeline_at_risk_usd: 19350.0,
    intent_signal: "Intent cooling — 20% prospects silent 30d — 8d since champion contact — composite 17",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    intent_risk: "moderate", intent_pattern: "timing_mismatch",
    intent_severity: "lukewarm", recommended_action: "re_engagement_sequence",
    engagement_decay_score: 18.0, champion_health_score: 20.0,
    buying_signal_score: 28.0, competitive_threat_score: 12.0,
    buyer_intent_composite: 20.3,
    has_intent_gap: false, requires_re_engagement: true,
    estimated_pipeline_at_risk_usd: 28350.0,
    intent_signal: "Timing mismatch — 22% prospects silent 30d — 9d since champion contact — composite 20",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    intent_risk: "high", intent_pattern: "competitor_evaluation",
    intent_severity: "cooling", recommended_action: "competitive_displacement",
    engagement_decay_score: 35.0, champion_health_score: 30.0,
    buying_signal_score: 38.0, competitive_threat_score: 42.0,
    buyer_intent_composite: 35.55,
    has_intent_gap: true, requires_re_engagement: true,
    estimated_pipeline_at_risk_usd: 71100.0,
    intent_signal: "Competitor evaluation — 35% prospects silent 30d — 12d since champion contact — 5 competitor mentions — composite 36",
  },
  {
    rep_id: "rep_006", region: "West",
    intent_risk: "high", intent_pattern: "ghost_prospect",
    intent_severity: "cooling", recommended_action: "re_engagement_sequence",
    engagement_decay_score: 45.0, champion_health_score: 35.0,
    buying_signal_score: 40.0, competitive_threat_score: 28.0,
    buyer_intent_composite: 38.45,
    has_intent_gap: true, requires_re_engagement: true,
    estimated_pipeline_at_risk_usd: 96750.0,
    intent_signal: "Ghost prospect — 40% prospects silent 30d — 15d since champion contact — composite 38",
  },
  {
    rep_id: "rep_007", region: "APAC",
    intent_risk: "critical", intent_pattern: "champion_disengagement",
    intent_severity: "ghosted", recommended_action: "champion_outreach",
    engagement_decay_score: 65.0, champion_health_score: 72.0,
    buying_signal_score: 58.0, competitive_threat_score: 50.0,
    buyer_intent_composite: 63.7,
    has_intent_gap: true, requires_re_engagement: true,
    estimated_pipeline_at_risk_usd: 243000.0,
    intent_signal: "Champion disengagement — 55% prospects silent 30d — 22d since champion contact — 6 competitor mentions — composite 64",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    intent_risk: "critical", intent_pattern: "champion_disengagement",
    intent_severity: "ghosted", recommended_action: "deal_rescue_escalation",
    engagement_decay_score: 80.0, champion_health_score: 85.0,
    buying_signal_score: 75.0, competitive_threat_score: 68.0,
    buyer_intent_composite: 79.05,
    has_intent_gap: true, requires_re_engagement: true,
    estimated_pipeline_at_risk_usd: 719280.0,
    intent_signal: "Champion disengagement — 60% prospects silent 30d — 25d since champion contact — 8 competitor mentions — composite 89",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-buyer-intent-signal-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.intent_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.intent_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_decay = 0, total_champ = 0, total_sig = 0, total_threat = 0, total_risk = 0;

  for (const r of mockReps) {
    risk_counts[r.intent_risk]       = (risk_counts[r.intent_risk] || 0) + 1;
    pattern_counts[r.intent_pattern] = (pattern_counts[r.intent_pattern] || 0) + 1;
    severity_counts[r.intent_severity] = (severity_counts[r.intent_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp   += r.buyer_intent_composite;
    total_decay  += r.engagement_decay_score;
    total_champ  += r.champion_health_score;
    total_sig    += r.buying_signal_score;
    total_threat += r.competitive_threat_score;
    total_risk   += r.estimated_pipeline_at_risk_usd;
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
      avg_buyer_intent_composite:               Math.round((total_comp / n) * 10) / 10,
      intent_gap_count:                         mockReps.filter((r) => r.has_intent_gap).length,
      re_engagement_count:                      mockReps.filter((r) => r.requires_re_engagement).length,
      avg_engagement_decay_score:               Math.round((total_decay / n) * 10) / 10,
      avg_champion_health_score:                Math.round((total_champ / n) * 10) / 10,
      avg_buying_signal_score:                  Math.round((total_sig / n) * 10) / 10,
      avg_competitive_threat_score:             Math.round((total_threat / n) * 10) / 10,
      total_estimated_pipeline_at_risk_usd:     Math.round(total_risk * 100) / 100,
    },
  });
}
