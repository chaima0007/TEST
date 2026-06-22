import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sales-multithreading-intelligence-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    multithread_risk: "low", multithread_pattern: "none",
    multithread_severity: "networked", recommended_action: "no_action",
    threading_breadth_score: 0.0, champion_dependency_score: 0.0,
    decision_maker_coverage_score: 0.0, relationship_map_score: 0.0,
    multithread_composite: 0.0,
    has_threading_gap: false, requires_multithread_coaching: false,
    estimated_at_risk_usd: 0.0,
    multithread_signal: "Stakeholder coverage healthy — multi-threading, champion strength, and executive access within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    multithread_risk: "low", multithread_pattern: "none",
    multithread_severity: "networked", recommended_action: "no_action",
    threading_breadth_score: 5.0, champion_dependency_score: 3.0,
    decision_maker_coverage_score: 4.0, relationship_map_score: 2.0,
    multithread_composite: 3.65,
    has_threading_gap: false, requires_multithread_coaching: false,
    estimated_at_risk_usd: 0.0,
    multithread_signal: "Stakeholder coverage healthy — multi-threading, champion strength, and executive access within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    multithread_risk: "moderate", multithread_pattern: "relationship_stagnation",
    multithread_severity: "developing", recommended_action: "multithread_coaching",
    threading_breadth_score: 18.0, champion_dependency_score: 15.0,
    decision_maker_coverage_score: 20.0, relationship_map_score: 28.0,
    multithread_composite: 19.75,
    has_threading_gap: false, requires_multithread_coaching: false,
    estimated_at_risk_usd: 12480.0,
    multithread_signal: "Relationship stagnation — 35% single-threaded deals — 38% executive access — 20% at-risk from champion loss — composite 20",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    multithread_risk: "moderate", multithread_pattern: "stakeholder_map_gap",
    multithread_severity: "developing", recommended_action: "multithread_coaching",
    threading_breadth_score: 22.0, champion_dependency_score: 18.0,
    decision_maker_coverage_score: 25.0, relationship_map_score: 35.0,
    multithread_composite: 23.75,
    has_threading_gap: false, requires_multithread_coaching: true,
    estimated_at_risk_usd: 21840.0,
    multithread_signal: "Stakeholder map gap — 40% single-threaded deals — 30% executive access — 25% at-risk from champion loss — composite 24",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    multithread_risk: "high", multithread_pattern: "executive_blind_spot",
    multithread_severity: "exposed", recommended_action: "executive_outreach_plan",
    threading_breadth_score: 42.0, champion_dependency_score: 30.0,
    decision_maker_coverage_score: 45.0, relationship_map_score: 28.0,
    multithread_composite: 37.0,
    has_threading_gap: true, requires_multithread_coaching: true,
    estimated_at_risk_usd: 66600.0,
    multithread_signal: "Executive blind spot — 55% single-threaded deals — 15% executive access — 35% at-risk from champion loss — composite 37",
  },
  {
    rep_id: "rep_006", region: "West",
    multithread_risk: "high", multithread_pattern: "champion_dependency",
    multithread_severity: "exposed", recommended_action: "champion_backup_strategy",
    threading_breadth_score: 38.0, champion_dependency_score: 55.0,
    decision_maker_coverage_score: 35.0, relationship_map_score: 40.0,
    multithread_composite: 42.25,
    has_threading_gap: true, requires_multithread_coaching: true,
    estimated_at_risk_usd: 97200.0,
    multithread_signal: "Champion dependency — 52% single-threaded deals — 20% executive access — 52% at-risk from champion loss — composite 42",
  },
  {
    rep_id: "rep_007", region: "APAC",
    multithread_risk: "critical", multithread_pattern: "single_threading",
    multithread_severity: "fragile", recommended_action: "multithread_coaching",
    threading_breadth_score: 75.0, champion_dependency_score: 65.0,
    decision_maker_coverage_score: 58.0, relationship_map_score: 70.0,
    multithread_composite: 67.45,
    has_threading_gap: true, requires_multithread_coaching: true,
    estimated_at_risk_usd: 168960.0,
    multithread_signal: "Single threading — 72% single-threaded deals — 10% executive access — 58% at-risk from champion loss — composite 67",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    multithread_risk: "critical", multithread_pattern: "single_threading",
    multithread_severity: "fragile", recommended_action: "multithread_coaching",
    threading_breadth_score: 90.0, champion_dependency_score: 80.0,
    decision_maker_coverage_score: 85.0, relationship_map_score: 88.0,
    multithread_composite: 85.55,
    has_threading_gap: true, requires_multithread_coaching: true,
    estimated_at_risk_usd: 220800.0,
    multithread_signal: "Single threading — 78% single-threaded deals — 8% executive access — 65% at-risk from champion loss — composite 86",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-multithreading-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.multithread_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.multithread_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_br = 0, total_ch = 0, total_dec = 0, total_rel = 0, total_impact = 0;

  for (const r of mockReps) {
    risk_counts[r.multithread_risk]       = (risk_counts[r.multithread_risk] || 0) + 1;
    pattern_counts[r.multithread_pattern] = (pattern_counts[r.multithread_pattern] || 0) + 1;
    severity_counts[r.multithread_severity] = (severity_counts[r.multithread_severity] || 0) + 1;
    action_counts[r.recommended_action]   = (action_counts[r.recommended_action] || 0) + 1;
    total_comp   += r.multithread_composite;
    total_br     += r.threading_breadth_score;
    total_ch     += r.champion_dependency_score;
    total_dec    += r.decision_maker_coverage_score;
    total_rel    += r.relationship_map_score;
    total_impact += r.estimated_at_risk_usd;
  }

  const n = mockReps.length;

  return sealResponse(NextResponse.json({
    reps,
    summary: {
      total:                                    n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_multithread_composite:                Math.round((total_comp / n) * 10) / 10,
      threading_gap_count:                      mockReps.filter((r) => r.has_threading_gap).length,
      coaching_count:                           mockReps.filter((r) => r.requires_multithread_coaching).length,
      avg_threading_breadth_score:              Math.round((total_br / n) * 10) / 10,
      avg_champion_dependency_score:            Math.round((total_ch / n) * 10) / 10,
      avg_decision_maker_coverage_score:        Math.round((total_dec / n) * 10) / 10,
      avg_relationship_map_score:               Math.round((total_rel / n) * 10) / 10,
      total_estimated_at_risk_usd:              Math.round(total_impact * 100) / 100,
    },
  }));
}
