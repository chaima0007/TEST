import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sales-decision-criteria-alignment-intelligence-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    criteria_risk: "low", criteria_pattern: "none",
    criteria_severity: "shaping", recommended_action: "no_action",
    discovery_score: 0.0, influence_score: 0.0,
    alignment_score: 0.0, competitive_score: 0.0,
    criteria_composite: 0.0,
    has_criteria_gap: false, requires_criteria_coaching: false,
    estimated_lost_revenue_usd: 0.0,
    criteria_signal: "Decision criteria alignment healthy — early discovery, influence, and competitive positioning within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    criteria_risk: "low", criteria_pattern: "none",
    criteria_severity: "shaping", recommended_action: "no_action",
    discovery_score: 3.0, influence_score: 4.0,
    alignment_score: 2.0, competitive_score: 5.0,
    criteria_composite: 3.35,
    has_criteria_gap: false, requires_criteria_coaching: false,
    estimated_lost_revenue_usd: 0.0,
    criteria_signal: "Decision criteria alignment healthy — early discovery, influence, and competitive positioning within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    criteria_risk: "moderate", criteria_pattern: "criteria_reactive_alignment",
    criteria_severity: "aligned", recommended_action: "criteria_mapping_coaching",
    discovery_score: 18.0, influence_score: 22.0,
    alignment_score: 20.0, competitive_score: 15.0,
    criteria_composite: 19.55,
    has_criteria_gap: false, requires_criteria_coaching: true,
    estimated_lost_revenue_usd: 48000.0,
    criteria_signal: "Criteria reactive alignment — 55% criteria documented early — 38% criteria influenced — 25% losses from criteria mismatch — composite 20",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    criteria_risk: "moderate", criteria_pattern: "criteria_coaching_gap",
    criteria_severity: "aligned", recommended_action: "criteria_mapping_coaching",
    discovery_score: 25.0, influence_score: 20.0,
    alignment_score: 22.0, competitive_score: 18.0,
    criteria_composite: 21.95,
    has_criteria_gap: false, requires_criteria_coaching: true,
    estimated_lost_revenue_usd: 96000.0,
    criteria_signal: "Criteria coaching gap — 42% criteria documented early — 30% criteria influenced — 32% losses from criteria mismatch — composite 22",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    criteria_risk: "high", criteria_pattern: "late_criteria_discovery",
    criteria_severity: "reactive", recommended_action: "early_discovery_process_coaching",
    discovery_score: 42.0, influence_score: 35.0,
    alignment_score: 38.0, competitive_score: 30.0,
    criteria_composite: 37.25,
    has_criteria_gap: false, requires_criteria_coaching: true,
    estimated_lost_revenue_usd: 216000.0,
    criteria_signal: "Late criteria discovery — 30% criteria documented early — 22% criteria influenced — 42% losses from criteria mismatch — composite 37",
  },
  {
    rep_id: "rep_006", region: "West",
    criteria_risk: "high", criteria_pattern: "competitive_criteria_disadvantage",
    criteria_severity: "reactive", recommended_action: "criteria_mapping_coaching",
    discovery_score: 38.0, influence_score: 40.0,
    alignment_score: 45.0, competitive_score: 52.0,
    criteria_composite: 42.05,
    has_criteria_gap: true, requires_criteria_coaching: true,
    estimated_lost_revenue_usd: 378000.0,
    criteria_signal: "Competitive criteria disadvantage — 25% criteria documented early — 18% criteria influenced — 52% losses from criteria mismatch — composite 42",
  },
  {
    rep_id: "rep_007", region: "APAC",
    criteria_risk: "critical", criteria_pattern: "scorecard_blind_pursuit",
    criteria_severity: "misaligned", recommended_action: "deal_qualification_review",
    discovery_score: 65.0, influence_score: 70.0,
    alignment_score: 62.0, competitive_score: 68.0,
    criteria_composite: 66.2,
    has_criteria_gap: true, requires_criteria_coaching: true,
    estimated_lost_revenue_usd: 840000.0,
    criteria_signal: "Scorecard blind pursuit — 12% criteria documented early — 10% criteria influenced — 65% losses from criteria mismatch — composite 66",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    criteria_risk: "critical", criteria_pattern: "scorecard_blind_pursuit",
    criteria_severity: "misaligned", recommended_action: "deal_qualification_review",
    discovery_score: 100.0, influence_score: 100.0,
    alignment_score: 100.0, competitive_score: 100.0,
    criteria_composite: 100.0,
    has_criteria_gap: true, requires_criteria_coaching: true,
    estimated_lost_revenue_usd: 4200000.0,
    criteria_signal: "Scorecard blind pursuit — 10% criteria documented early — 8% criteria influenced — 70% losses from criteria mismatch — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-decision-criteria-alignment-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.criteria_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.criteria_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_dis = 0, total_inf = 0, total_ali = 0, total_com = 0, total_loss = 0;

  for (const r of mockReps) {
    risk_counts[r.criteria_risk]       = (risk_counts[r.criteria_risk] || 0) + 1;
    pattern_counts[r.criteria_pattern] = (pattern_counts[r.criteria_pattern] || 0) + 1;
    severity_counts[r.criteria_severity] = (severity_counts[r.criteria_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.criteria_composite;
    total_dis  += r.discovery_score;
    total_inf  += r.influence_score;
    total_ali  += r.alignment_score;
    total_com  += r.competitive_score;
    total_loss += r.estimated_lost_revenue_usd;
  }

  const n = mockReps.length;

  return sealResponse(NextResponse.json({
    reps,
    summary: {
      total:                                  n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_criteria_composite:                 Math.round((total_comp / n) * 10) / 10,
      criteria_gap_count:                     mockReps.filter((r) => r.has_criteria_gap).length,
      coaching_count:                         mockReps.filter((r) => r.requires_criteria_coaching).length,
      avg_discovery_score:                    Math.round((total_dis / n) * 10) / 10,
      avg_influence_score:                    Math.round((total_inf / n) * 10) / 10,
      avg_alignment_score:                    Math.round((total_ali / n) * 10) / 10,
      avg_competitive_score:                  Math.round((total_com / n) * 10) / 10,
      total_estimated_lost_revenue_usd:       Math.round(total_loss * 100) / 100,
    },
  }));
}
