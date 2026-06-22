import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[quota-gap-analysis] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "r_001",
    rep_name: "Alice Martin",
    manager_id: "m_001",
    region: "EMEA",
    segment: "enterprise",
    period_quota: 300000,
    effective_quota: 300000,
    closed_won_value: 180000,
    pipeline_value: 350000,
    late_stage_value: 150000,
    gap_to_quota: 120000,
    attainment_pct: 60.0,
    attainment_tier: "behind",
    projected_attainment: 89.5,
    gap_risk: "high",
    pipeline_coverage: "adequate",
    recommended_action: "focus_late_stage",
    required_win_rate: 0.343,
    deals_needed: 2,
    quota_achievement_score: 51.8,
    pipeline_health_score: 62.0,
    is_at_risk: true,
    days_remaining: 30,
    deals_in_pipeline: 6,
    avg_deal_size: 60000,
    win_rate: 0.35,
    is_ramping: false,
  },
  {
    rep_id: "r_002",
    rep_name: "Bruno Santos",
    manager_id: "m_001",
    region: "EMEA",
    segment: "mid_market",
    period_quota: 200000,
    effective_quota: 200000,
    closed_won_value: 235000,
    pipeline_value: 180000,
    late_stage_value: 90000,
    gap_to_quota: 0,
    attainment_pct: 117.5,
    attainment_tier: "overachiever",
    projected_attainment: 142.0,
    gap_risk: "low",
    pipeline_coverage: "strong",
    recommended_action: "celebrate_and_expand",
    required_win_rate: 0.0,
    deals_needed: 0,
    quota_achievement_score: 84.3,
    pipeline_health_score: 78.0,
    is_at_risk: false,
    days_remaining: 30,
    deals_in_pipeline: 5,
    avg_deal_size: 40000,
    win_rate: 0.48,
    is_ramping: false,
  },
  {
    rep_id: "r_003",
    rep_name: "Claire Dupont",
    manager_id: "m_002",
    region: "APAC",
    segment: "smb",
    period_quota: 120000,
    effective_quota: 90000,
    closed_won_value: 62000,
    pipeline_value: 140000,
    late_stage_value: 55000,
    gap_to_quota: 28000,
    attainment_pct: 68.9,
    attainment_tier: "at_risk",
    projected_attainment: 95.2,
    gap_risk: "medium",
    pipeline_coverage: "strong",
    recommended_action: "accelerate_pipeline",
    required_win_rate: 0.2,
    deals_needed: 2,
    quota_achievement_score: 58.4,
    pipeline_health_score: 67.5,
    is_at_risk: false,
    days_remaining: 45,
    deals_in_pipeline: 8,
    avg_deal_size: 18000,
    win_rate: 0.38,
    is_ramping: true,
  },
  {
    rep_id: "r_004",
    rep_name: "David Chen",
    manager_id: "m_002",
    region: "APAC",
    segment: "enterprise",
    period_quota: 350000,
    effective_quota: 350000,
    closed_won_value: 95000,
    pipeline_value: 220000,
    late_stage_value: 80000,
    gap_to_quota: 255000,
    attainment_pct: 27.1,
    attainment_tier: "critical",
    projected_attainment: 42.8,
    gap_risk: "critical",
    pipeline_coverage: "thin",
    recommended_action: "executive_intervention",
    required_win_rate: 1.0,
    deals_needed: 5,
    quota_achievement_score: 22.1,
    pipeline_health_score: 31.0,
    is_at_risk: true,
    days_remaining: 18,
    deals_in_pipeline: 4,
    avg_deal_size: 55000,
    win_rate: 0.22,
    is_ramping: false,
  },
  {
    rep_id: "r_005",
    rep_name: "Eva Rodriguez",
    manager_id: "m_001",
    region: "Americas",
    segment: "mid_market",
    period_quota: 220000,
    effective_quota: 220000,
    closed_won_value: 198000,
    pipeline_value: 160000,
    late_stage_value: 95000,
    gap_to_quota: 22000,
    attainment_pct: 90.0,
    attainment_tier: "on_track",
    projected_attainment: 108.5,
    gap_risk: "low",
    pipeline_coverage: "strong",
    recommended_action: "maintain_pace",
    required_win_rate: 0.138,
    deals_needed: 1,
    quota_achievement_score: 73.6,
    pipeline_health_score: 71.0,
    is_at_risk: false,
    days_remaining: 28,
    deals_in_pipeline: 5,
    avg_deal_size: 35000,
    win_rate: 0.42,
    is_ramping: false,
  },
  {
    rep_id: "r_006",
    rep_name: "Félix Moreau",
    manager_id: "m_003",
    region: "EMEA",
    segment: "enterprise",
    period_quota: 400000,
    effective_quota: 400000,
    closed_won_value: 185000,
    pipeline_value: 580000,
    late_stage_value: 220000,
    gap_to_quota: 215000,
    attainment_pct: 46.3,
    attainment_tier: "behind",
    projected_attainment: 78.4,
    gap_risk: "high",
    pipeline_coverage: "adequate",
    recommended_action: "focus_late_stage",
    required_win_rate: 0.371,
    deals_needed: 4,
    quota_achievement_score: 44.2,
    pipeline_health_score: 58.5,
    is_at_risk: true,
    days_remaining: 35,
    deals_in_pipeline: 9,
    avg_deal_size: 65000,
    win_rate: 0.31,
    is_ramping: false,
  },
  {
    rep_id: "r_007",
    rep_name: "Grace Kim",
    manager_id: "m_003",
    region: "APAC",
    segment: "smb",
    period_quota: 100000,
    effective_quota: 75000,
    closed_won_value: 58000,
    pipeline_value: 95000,
    late_stage_value: 42000,
    gap_to_quota: 17000,
    attainment_pct: 77.3,
    attainment_tier: "at_risk",
    projected_attainment: 101.6,
    gap_risk: "medium",
    pipeline_coverage: "strong",
    recommended_action: "accelerate_pipeline",
    required_win_rate: 0.179,
    deals_needed: 1,
    quota_achievement_score: 61.7,
    pipeline_health_score: 65.0,
    is_at_risk: false,
    days_remaining: 40,
    deals_in_pipeline: 7,
    avg_deal_size: 18000,
    win_rate: 0.36,
    is_ramping: true,
  },
  {
    rep_id: "r_008",
    rep_name: "Hassan Ali",
    manager_id: "m_002",
    region: "Americas",
    segment: "mid_market",
    period_quota: 250000,
    effective_quota: 250000,
    closed_won_value: 45000,
    pipeline_value: 180000,
    late_stage_value: 60000,
    gap_to_quota: 205000,
    attainment_pct: 18.0,
    attainment_tier: "critical",
    projected_attainment: 35.2,
    gap_risk: "critical",
    pipeline_coverage: "insufficient",
    recommended_action: "executive_intervention",
    required_win_rate: 1.0,
    deals_needed: 5,
    quota_achievement_score: 15.8,
    pipeline_health_score: 28.0,
    is_at_risk: true,
    days_remaining: 14,
    deals_in_pipeline: 4,
    avg_deal_size: 42000,
    win_rate: 0.18,
    is_ramping: false,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const tier    = searchParams.get("tier");
  const risk    = searchParams.get("risk");
  const manager = searchParams.get("manager");
  const region  = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/quota-gap-analysis`);
      if (tier)    url.searchParams.set("tier", tier);
      if (risk)    url.searchParams.set("risk", risk);
      if (manager) url.searchParams.set("manager", manager);
      if (region)  url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let reps = [...mockReps];
  if (tier)    reps = reps.filter((r) => r.attainment_tier === tier);
  if (risk)    reps = reps.filter((r) => r.gap_risk === risk);
  if (manager) reps = reps.filter((r) => r.manager_id === manager);
  if (region)  reps = reps.filter((r) => r.region === region);

  const tier_counts:     Record<string, number> = {};
  const risk_counts:     Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  const coverage_counts: Record<string, number> = {};
  let total_att = 0, total_proj = 0, total_ach = 0, total_pipe_h = 0, total_gap = 0;

  for (const r of mockReps) {
    tier_counts[r.attainment_tier]     = (tier_counts[r.attainment_tier] || 0) + 1;
    risk_counts[r.gap_risk]            = (risk_counts[r.gap_risk] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    coverage_counts[r.pipeline_coverage] = (coverage_counts[r.pipeline_coverage] || 0) + 1;
    total_att    += r.attainment_pct;
    total_proj   += r.projected_attainment;
    total_ach    += r.quota_achievement_score;
    total_pipe_h += r.pipeline_health_score;
    total_gap    += r.gap_to_quota;
  }

  const n = mockReps.length;

  return sealResponse(NextResponse.json({
    reps,
    summary: {
      total:                       n,
      tier_counts,
      risk_counts,
      action_counts,
      coverage_counts,
      avg_attainment_pct:          Math.round((total_att / n) * 10) / 10,
      avg_projected_attainment:    Math.round((total_proj / n) * 10) / 10,
      avg_achievement_score:       Math.round((total_ach / n) * 10) / 10,
      avg_pipeline_health_score:   Math.round((total_pipe_h / n) * 10) / 10,
      total_gap:                   Math.round(total_gap * 100) / 100,
      at_risk_count:               mockReps.filter((r) => r.is_at_risk).length,
      overachiever_count:          mockReps.filter((r) => r.attainment_tier === "overachiever").length,
      critical_count:              mockReps.filter((r) => r.gap_risk === "critical").length,
    },
  }));
}
