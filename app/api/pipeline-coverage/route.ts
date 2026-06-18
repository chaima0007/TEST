import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockTeams = [
  {
    team_id: "t_001", region: "EMEA", segment: "enterprise", manager_id: "mgr_001",
    coverage_status: "over_covered", gap_severity: "none",
    pipeline_quality: "good", coverage_action: "maintain",
    coverage_ratio: 3.8, weighted_coverage_ratio: 1.42, gap_to_quota: 0,
    pipeline_velocity: 9800, quality_score: 68.0, stage_mix_score: 52.0,
    coverage_trend: 28.5, is_at_risk: false, needs_intervention: false,
    quota_remaining: 800000, current_pipeline: 3040000, weighted_pipeline: 1136000,
    avg_deal_health: 74.0, stalled_deal_count: 2, competitive_deal_pct: 28.0,
  },
  {
    team_id: "t_002", region: "NAMER", segment: "mid-market", manager_id: "mgr_002",
    coverage_status: "adequate", gap_severity: "none",
    pipeline_quality: "excellent", coverage_action: "maintain",
    coverage_ratio: 2.6, weighted_coverage_ratio: 1.18, gap_to_quota: 0,
    pipeline_velocity: 12500, quality_score: 78.0, stage_mix_score: 61.0,
    coverage_trend: 35.2, is_at_risk: false, needs_intervention: false,
    quota_remaining: 600000, current_pipeline: 1560000, weighted_pipeline: 708000,
    avg_deal_health: 80.0, stalled_deal_count: 1, competitive_deal_pct: 22.0,
  },
  {
    team_id: "t_003", region: "APAC", segment: "enterprise", manager_id: "mgr_003",
    coverage_status: "under_covered", gap_severity: "medium",
    pipeline_quality: "fair", coverage_action: "accelerate_existing",
    coverage_ratio: 1.6, weighted_coverage_ratio: 0.72, gap_to_quota: 280000,
    pipeline_velocity: 5200, quality_score: 44.0, stage_mix_score: 38.0,
    coverage_trend: -12.0, is_at_risk: true, needs_intervention: false,
    quota_remaining: 1000000, current_pipeline: 1600000, weighted_pipeline: 720000,
    avg_deal_health: 55.0, stalled_deal_count: 6, competitive_deal_pct: 48.0,
  },
  {
    team_id: "t_004", region: "LATAM", segment: "smb", manager_id: "mgr_004",
    coverage_status: "critical_gap", gap_severity: "critical",
    pipeline_quality: "poor", coverage_action: "generate_pipeline",
    coverage_ratio: 0.7, weighted_coverage_ratio: 0.31, gap_to_quota: 414000,
    pipeline_velocity: 1800, quality_score: 22.0, stage_mix_score: 18.0,
    coverage_trend: -42.0, is_at_risk: true, needs_intervention: true,
    quota_remaining: 600000, current_pipeline: 420000, weighted_pipeline: 186000,
    avg_deal_health: 28.0, stalled_deal_count: 12, competitive_deal_pct: 65.0,
  },
  {
    team_id: "t_005", region: "EMEA", segment: "mid-market", manager_id: "mgr_001",
    coverage_status: "adequate", gap_severity: "low",
    pipeline_quality: "good", coverage_action: "maintain",
    coverage_ratio: 2.2, weighted_coverage_ratio: 0.92, gap_to_quota: 56000,
    pipeline_velocity: 7600, quality_score: 62.0, stage_mix_score: 48.0,
    coverage_trend: 18.0, is_at_risk: false, needs_intervention: false,
    quota_remaining: 700000, current_pipeline: 1540000, weighted_pipeline: 644000,
    avg_deal_health: 68.0, stalled_deal_count: 3, competitive_deal_pct: 32.0,
  },
  {
    team_id: "t_006", region: "NAMER", segment: "enterprise", manager_id: "mgr_002",
    coverage_status: "over_covered", gap_severity: "none",
    pipeline_quality: "excellent", coverage_action: "expand_upmarket",
    coverage_ratio: 4.2, weighted_coverage_ratio: 1.88, gap_to_quota: 0,
    pipeline_velocity: 18000, quality_score: 82.0, stage_mix_score: 68.0,
    coverage_trend: 55.0, is_at_risk: false, needs_intervention: false,
    quota_remaining: 900000, current_pipeline: 3780000, weighted_pipeline: 1692000,
    avg_deal_health: 84.0, stalled_deal_count: 1, competitive_deal_pct: 18.0,
  },
  {
    team_id: "t_007", region: "APAC", segment: "smb", manager_id: "mgr_003",
    coverage_status: "under_covered", gap_severity: "high",
    pipeline_quality: "fair", coverage_action: "reallocate",
    coverage_ratio: 1.2, weighted_coverage_ratio: 0.54, gap_to_quota: 230000,
    pipeline_velocity: 3100, quality_score: 38.0, stage_mix_score: 25.0,
    coverage_trend: -28.0, is_at_risk: true, needs_intervention: false,
    quota_remaining: 500000, current_pipeline: 600000, weighted_pipeline: 270000,
    avg_deal_health: 42.0, stalled_deal_count: 8, competitive_deal_pct: 55.0,
  },
  {
    team_id: "t_008", region: "EMEA", segment: "enterprise", manager_id: "mgr_005",
    coverage_status: "adequate", gap_severity: "none",
    pipeline_quality: "good", coverage_action: "maintain",
    coverage_ratio: 2.4, weighted_coverage_ratio: 1.08, gap_to_quota: 0,
    pipeline_velocity: 8900, quality_score: 65.0, stage_mix_score: 55.0,
    coverage_trend: 22.0, is_at_risk: false, needs_intervention: false,
    quota_remaining: 750000, current_pipeline: 1800000, weighted_pipeline: 810000,
    avg_deal_health: 70.0, stalled_deal_count: 2, competitive_deal_pct: 30.0,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const status  = searchParams.get("status");
  const gap     = searchParams.get("gap");
  const region  = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/pipeline-coverage`);
      if (status) url.searchParams.set("status", status);
      if (gap)    url.searchParams.set("gap", gap);
      if (region) url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let teams = [...mockTeams];
  if (status) teams = teams.filter((t) => t.coverage_status === status);
  if (gap)    teams = teams.filter((t) => t.gap_severity === gap);
  if (region) teams = teams.filter((t) => t.region === region);

  const status_counts:  Record<string, number> = {};
  const gap_counts:     Record<string, number> = {};
  const quality_counts: Record<string, number> = {};
  const action_counts:  Record<string, number> = {};
  let total_coverage = 0, total_w_coverage = 0,
      total_quality = 0, total_stage_mix = 0;

  for (const t of mockTeams) {
    status_counts[t.coverage_status]   = (status_counts[t.coverage_status] || 0) + 1;
    gap_counts[t.gap_severity]         = (gap_counts[t.gap_severity] || 0) + 1;
    quality_counts[t.pipeline_quality] = (quality_counts[t.pipeline_quality] || 0) + 1;
    action_counts[t.coverage_action]   = (action_counts[t.coverage_action] || 0) + 1;
    total_coverage   += t.coverage_ratio;
    total_w_coverage += t.weighted_coverage_ratio;
    total_quality    += t.quality_score;
    total_stage_mix  += t.stage_mix_score;
  }

  const n = mockTeams.length;

  return NextResponse.json({
    teams,
    summary: {
      total:                    n,
      status_counts,
      gap_severity_counts:      gap_counts,
      quality_counts,
      action_counts,
      avg_coverage_ratio:       Math.round((total_coverage / n) * 100) / 100,
      avg_weighted_coverage:    Math.round((total_w_coverage / n) * 100) / 100,
      total_gap_to_quota:       mockTeams.reduce((s, t) => s + t.gap_to_quota, 0),
      at_risk_count:            mockTeams.filter((t) => t.is_at_risk).length,
      intervention_count:       mockTeams.filter((t) => t.needs_intervention).length,
      avg_quality_score:        Math.round((total_quality / n) * 10) / 10,
      avg_stage_mix_score:      Math.round((total_stage_mix / n) * 10) / 10,
      healthy_team_count:       mockTeams.filter((t) =>
        t.coverage_status === "over_covered" || t.coverage_status === "adequate"
      ).length,
    },
  });
}
