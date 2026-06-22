import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sales-discovery-quality-intelligence-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    discovery_risk: "low", discovery_pattern: "none",
    discovery_severity: "thorough", recommended_action: "no_action",
    depth_score: 0.0, qualification_score: 0.0,
    stakeholder_score: 0.0, fit_score: 0.0,
    discovery_composite: 0.0,
    has_discovery_gap: false, requires_discovery_coaching: false,
    estimated_wasted_pipeline_usd: 0.0,
    discovery_signal: "Discovery quality strong — depth of questioning, qualification, and stakeholder mapping within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    discovery_risk: "low", discovery_pattern: "none",
    discovery_severity: "thorough", recommended_action: "no_action",
    depth_score: 3.0, qualification_score: 4.0,
    stakeholder_score: 2.0, fit_score: 5.0,
    discovery_composite: 3.5,
    has_discovery_gap: false, requires_discovery_coaching: false,
    estimated_wasted_pipeline_usd: 0.0,
    discovery_signal: "Discovery quality strong — depth of questioning, qualification, and stakeholder mapping within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    discovery_risk: "moderate", discovery_pattern: "none",
    discovery_severity: "adequate", recommended_action: "discovery_framework_coaching",
    depth_score: 22.0, qualification_score: 20.0,
    stakeholder_score: 22.0, fit_score: 18.0,
    discovery_composite: 21.2,
    has_discovery_gap: true, requires_discovery_coaching: true,
    estimated_wasted_pipeline_usd: 42000.0,
    discovery_signal: "Discovery risk — 9 avg questions per call — 55% budget qualified before demo — 18% deals lost to poor fit — composite 21",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    discovery_risk: "moderate", discovery_pattern: "budget_avoidance",
    discovery_severity: "adequate", recommended_action: "discovery_framework_coaching",
    depth_score: 28.0, qualification_score: 35.0,
    stakeholder_score: 25.0, fit_score: 20.0,
    discovery_composite: 28.0,
    has_discovery_gap: true, requires_discovery_coaching: true,
    estimated_wasted_pipeline_usd: 81000.0,
    discovery_signal: "Budget avoidance — 8 avg questions per call — 35% budget qualified before demo — 22% deals lost to poor fit — composite 28",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    discovery_risk: "high", discovery_pattern: "single_stakeholder_lock",
    discovery_severity: "shallow", recommended_action: "stakeholder_mapping_coaching",
    depth_score: 40.0, qualification_score: 42.0,
    stakeholder_score: 55.0, fit_score: 35.0,
    discovery_composite: 43.5,
    has_discovery_gap: true, requires_pipeline_coaching: true,
    estimated_wasted_pipeline_usd: 210000.0,
    discovery_signal: "Single stakeholder lock — 7 avg questions per call — 30% budget qualified before demo — 28% deals lost to poor fit — composite 44",
  },
  {
    rep_id: "rep_006", region: "West",
    discovery_risk: "high", discovery_pattern: "pain_point_skipping",
    discovery_severity: "shallow", recommended_action: "discovery_framework_coaching",
    depth_score: 52.0, qualification_score: 45.0,
    stakeholder_score: 48.0, fit_score: 42.0,
    discovery_composite: 47.7,
    has_discovery_gap: true, requires_discovery_coaching: true,
    estimated_wasted_pipeline_usd: 352000.0,
    discovery_signal: "Pain point skipping — 6 avg questions per call — 28% budget qualified before demo — 32% deals lost to poor fit — composite 48",
  },
  {
    rep_id: "rep_007", region: "APAC",
    discovery_risk: "critical", discovery_pattern: "premature_solutioning",
    discovery_severity: "negligent", recommended_action: "discovery_framework_coaching",
    depth_score: 78.0, qualification_score: 72.0,
    stakeholder_score: 68.0, fit_score: 65.0,
    discovery_composite: 71.8,
    has_discovery_gap: true, requires_discovery_coaching: true,
    estimated_wasted_pipeline_usd: 1080000.0,
    discovery_signal: "Premature solutioning — 4 avg questions per call — 15% budget qualified before demo — 45% deals lost to poor fit — composite 72",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    discovery_risk: "critical", discovery_pattern: "premature_solutioning",
    discovery_severity: "negligent", recommended_action: "discovery_reset_intervention",
    depth_score: 100.0, qualification_score: 100.0,
    stakeholder_score: 100.0, fit_score: 100.0,
    discovery_composite: 100.0,
    has_discovery_gap: true, requires_discovery_coaching: true,
    estimated_wasted_pipeline_usd: 2400000.0,
    discovery_signal: "Premature solutioning — 3 avg questions per call — 15% budget qualified before demo — 50% deals lost to poor fit — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-discovery-quality-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.discovery_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.discovery_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_dep = 0, total_qua = 0, total_sta = 0, total_fit = 0, total_loss = 0;

  for (const r of mockReps) {
    risk_counts[r.discovery_risk]         = (risk_counts[r.discovery_risk] || 0) + 1;
    pattern_counts[r.discovery_pattern]   = (pattern_counts[r.discovery_pattern] || 0) + 1;
    severity_counts[r.discovery_severity] = (severity_counts[r.discovery_severity] || 0) + 1;
    action_counts[r.recommended_action]   = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.discovery_composite;
    total_dep  += r.depth_score;
    total_qua  += r.qualification_score;
    total_sta  += r.stakeholder_score;
    total_fit  += r.fit_score;
    total_loss += r.estimated_wasted_pipeline_usd;
  }

  const n = mockReps.length;

  return sealResponse(NextResponse.json({
    reps,
    summary: {
      total:                                   n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_discovery_composite:                 Math.round((total_comp / n) * 10) / 10,
      discovery_gap_count:                     mockReps.filter((r) => r.has_discovery_gap).length,
      coaching_count:                          mockReps.filter((r) => r.requires_discovery_coaching).length,
      avg_depth_score:                         Math.round((total_dep / n) * 10) / 10,
      avg_qualification_score:                 Math.round((total_qua / n) * 10) / 10,
      avg_stakeholder_score:                   Math.round((total_sta / n) * 10) / 10,
      avg_fit_score:                           Math.round((total_fit / n) * 10) / 10,
      total_estimated_wasted_pipeline_usd:     Math.round(total_loss * 100) / 100,
    },
  }));
}
