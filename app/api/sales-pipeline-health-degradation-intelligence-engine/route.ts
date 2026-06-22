import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sales-pipeline-health-degradation-intelligence-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    pipeline_risk: "low", pipeline_pattern: "none",
    pipeline_severity: "healthy", recommended_action: "no_action",
    staleness_score: 0.0, progression_score: 0.0,
    curation_score: 0.0, concentration_score: 0.0,
    pipeline_composite: 0.0,
    has_pipeline_gap: false, requires_pipeline_coaching: false,
    estimated_phantom_pipeline_usd: 0.0,
    pipeline_signal: "Pipeline health strong — deal activity, stage progression, and curation within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    pipeline_risk: "low", pipeline_pattern: "none",
    pipeline_severity: "healthy", recommended_action: "no_action",
    staleness_score: 3.0, progression_score: 4.0,
    curation_score: 2.0, concentration_score: 5.0,
    pipeline_composite: 3.5,
    has_pipeline_gap: false, requires_pipeline_coaching: false,
    estimated_phantom_pipeline_usd: 0.0,
    pipeline_signal: "Pipeline health strong — deal activity, stage progression, and curation within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    pipeline_risk: "moderate", pipeline_pattern: "none",
    pipeline_severity: "declining", recommended_action: "pipeline_hygiene_coaching",
    staleness_score: 22.0, progression_score: 20.0,
    curation_score: 22.0, concentration_score: 18.0,
    pipeline_composite: 21.2,
    has_pipeline_gap: false, requires_pipeline_coaching: true,
    estimated_phantom_pipeline_usd: 23850.0,
    pipeline_signal: "Pipeline risk — 12% deals with no activity 30d — 58% stage progression rate — 38% pipeline converting to wins — composite 21",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    pipeline_risk: "moderate", pipeline_pattern: "curation_avoidance",
    pipeline_severity: "declining", recommended_action: "pipeline_hygiene_coaching",
    staleness_score: 30.0, progression_score: 25.0,
    curation_score: 30.0, concentration_score: 22.0,
    pipeline_composite: 27.3,
    has_pipeline_gap: false, requires_pipeline_coaching: true,
    estimated_phantom_pipeline_usd: 56700.0,
    pipeline_signal: "Curation avoidance — 20% deals with no activity 30d — 52% stage progression rate — 32% pipeline converting to wins — composite 27",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    pipeline_risk: "high", pipeline_pattern: "stage_stagnation",
    pipeline_severity: "degraded", recommended_action: "stage_exit_criteria_coaching",
    staleness_score: 40.0, progression_score: 45.0,
    curation_score: 40.0, concentration_score: 35.0,
    pipeline_composite: 41.2,
    has_pipeline_gap: true, requires_pipeline_coaching: true,
    estimated_phantom_pipeline_usd: 198275.0,
    pipeline_signal: "Stage stagnation — 35% deals with no activity 30d — 35% stage progression rate — 25% pipeline converting to wins — composite 41",
  },
  {
    rep_id: "rep_006", region: "West",
    pipeline_risk: "high", pipeline_pattern: "curation_avoidance",
    pipeline_severity: "degraded", recommended_action: "pipeline_hygiene_coaching",
    staleness_score: 55.0, progression_score: 48.0,
    curation_score: 50.0, concentration_score: 42.0,
    pipeline_composite: 49.9,
    has_pipeline_gap: true, requires_pipeline_coaching: true,
    estimated_phantom_pipeline_usd: 329340.0,
    pipeline_signal: "Curation avoidance — 42% deals with no activity 30d — 30% stage progression rate — 22% pipeline converting to wins — composite 50",
  },
  {
    rep_id: "rep_007", region: "APAC",
    pipeline_risk: "critical", pipeline_pattern: "zombie_deal_accumulation",
    pipeline_severity: "critical", recommended_action: "pipeline_hygiene_coaching",
    staleness_score: 80.0, progression_score: 75.0,
    curation_score: 68.0, concentration_score: 55.0,
    pipeline_composite: 71.8,
    has_pipeline_gap: true, requires_pipeline_coaching: true,
    estimated_phantom_pipeline_usd: 817025.0,
    pipeline_signal: "Zombie deal accumulation — 55% deals with no activity 30d — 20% stage progression rate — 12% pipeline converting to wins — composite 72",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    pipeline_risk: "critical", pipeline_pattern: "pipeline_inflation",
    pipeline_severity: "critical", recommended_action: "pipeline_curation_workshop",
    staleness_score: 100.0, progression_score: 100.0,
    curation_score: 100.0, concentration_score: 100.0,
    pipeline_composite: 100.0,
    has_pipeline_gap: true, requires_pipeline_coaching: true,
    estimated_phantom_pipeline_usd: 2025000.0,
    pipeline_signal: "Pipeline inflation — 62% deals with no activity 30d — 15% stage progression rate — 8% pipeline converting to wins — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-pipeline-health-degradation-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.pipeline_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.pipeline_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_sta = 0, total_pro = 0, total_cur = 0, total_con = 0, total_loss = 0;

  for (const r of mockReps) {
    risk_counts[r.pipeline_risk]         = (risk_counts[r.pipeline_risk] || 0) + 1;
    pattern_counts[r.pipeline_pattern]   = (pattern_counts[r.pipeline_pattern] || 0) + 1;
    severity_counts[r.pipeline_severity] = (severity_counts[r.pipeline_severity] || 0) + 1;
    action_counts[r.recommended_action]  = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.pipeline_composite;
    total_sta  += r.staleness_score;
    total_pro  += r.progression_score;
    total_cur  += r.curation_score;
    total_con  += r.concentration_score;
    total_loss += r.estimated_phantom_pipeline_usd;
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
      avg_pipeline_composite:                   Math.round((total_comp / n) * 10) / 10,
      pipeline_gap_count:                       mockReps.filter((r) => r.has_pipeline_gap).length,
      coaching_count:                           mockReps.filter((r) => r.requires_pipeline_coaching).length,
      avg_staleness_score:                      Math.round((total_sta / n) * 10) / 10,
      avg_progression_score:                    Math.round((total_pro / n) * 10) / 10,
      avg_curation_score:                       Math.round((total_cur / n) * 10) / 10,
      avg_concentration_score:                  Math.round((total_con / n) * 10) / 10,
      total_estimated_phantom_pipeline_usd:     Math.round(total_loss * 100) / 100,
    },
  }));
}
