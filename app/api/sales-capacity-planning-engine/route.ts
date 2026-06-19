import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockRegions = [
  {
    region_id: "reg_001", region_name: "NAMER West", region_head: "John Smith",
    capacity_status: "critical_gap", capacity_risk: "high",
    growth_constraint: "headcount", capacity_action: "accelerate_hiring",
    required_headcount: 12, capacity_gap: 4,
    productivity_score: 77.0, pipeline_health_score: 82.0, hiring_efficiency_score: 70.0,
    capacity_composite: 77.1, is_understaffed: true,
    revenue_at_risk_usd: 4800000.0,
    capacity_signal: "headcount gap of 4 reps against target — accelerate recruiting",
    annual_revenue_target_usd: 14400000.0,
    current_headcount: 8,
  },
  {
    region_id: "reg_002", region_name: "EMEA North", region_head: "Sophie Müller",
    capacity_status: "critical_gap", capacity_risk: "critical",
    growth_constraint: "hiring_speed", capacity_action: "accelerate_hiring",
    required_headcount: 15, capacity_gap: 7,
    productivity_score: 28.0, pipeline_health_score: 32.0, hiring_efficiency_score: 15.0,
    capacity_composite: 26.1, is_understaffed: true,
    revenue_at_risk_usd: 9800000.0,
    capacity_signal: "hiring bottleneck — avg 110 days to hire with 7 open roles needed",
    annual_revenue_target_usd: 18000000.0,
    current_headcount: 8,
  },
  {
    region_id: "reg_003", region_name: "APAC South", region_head: "Kenji Nakamura",
    capacity_status: "balanced", capacity_risk: "low",
    growth_constraint: "none", capacity_action: "maintain",
    required_headcount: 10, capacity_gap: 0,
    productivity_score: 88.0, pipeline_health_score: 85.0, hiring_efficiency_score: 90.0,
    capacity_composite: 87.5, is_understaffed: false,
    revenue_at_risk_usd: 420000.0,
    capacity_signal: "capacity balanced — 10 reps supporting 12.0M target",
    annual_revenue_target_usd: 12000000.0,
    current_headcount: 10,
  },
  {
    region_id: "reg_004", region_name: "LATAM", region_head: "Maria Gonzalez",
    capacity_status: "gap", capacity_risk: "moderate",
    growth_constraint: "pipeline", capacity_action: "restructure_territory",
    required_headcount: 8, capacity_gap: 2,
    productivity_score: 52.0, pipeline_health_score: 38.0, hiring_efficiency_score: 65.0,
    capacity_composite: 50.1, is_understaffed: true,
    revenue_at_risk_usd: 2600000.0,
    capacity_signal: "pipeline coverage 1.8x — insufficient to support target attainment",
    annual_revenue_target_usd: 8000000.0,
    current_headcount: 6,
  },
  {
    region_id: "reg_005", region_name: "NAMER East", region_head: "Robert Chen",
    capacity_status: "surplus", capacity_risk: "low",
    growth_constraint: "none", capacity_action: "maintain",
    required_headcount: 9, capacity_gap: -3,
    productivity_score: 92.0, pipeline_health_score: 88.0, hiring_efficiency_score: 95.0,
    capacity_composite: 91.4, is_understaffed: false,
    revenue_at_risk_usd: 185000.0,
    capacity_signal: "surplus of 3 reps — consider territory expansion or increased quotas",
    annual_revenue_target_usd: 10800000.0,
    current_headcount: 12,
  },
  {
    region_id: "reg_006", region_name: "EMEA South", region_head: "Antoine Dubois",
    capacity_status: "gap", capacity_risk: "high",
    growth_constraint: "productivity", capacity_action: "accelerate_hiring",
    required_headcount: 11, capacity_gap: 3,
    productivity_score: 35.0, pipeline_health_score: 48.0, hiring_efficiency_score: 42.0,
    capacity_composite: 40.0, is_understaffed: true,
    revenue_at_risk_usd: 3900000.0,
    capacity_signal: "rep productivity at 52% — headcount increase won't solve attainment issue",
    annual_revenue_target_usd: 13200000.0,
    current_headcount: 8,
  },
  {
    region_id: "reg_007", region_name: "APAC North", region_head: "Priya Patel",
    capacity_status: "balanced", capacity_risk: "moderate",
    growth_constraint: "pipeline", capacity_action: "restructure_territory",
    required_headcount: 7, capacity_gap: 0,
    productivity_score: 60.0, pipeline_health_score: 42.0, hiring_efficiency_score: 72.0,
    capacity_composite: 57.1, is_understaffed: false,
    revenue_at_risk_usd: 890000.0,
    capacity_signal: "pipeline coverage 2.2x — insufficient to support target attainment",
    annual_revenue_target_usd: 8400000.0,
    current_headcount: 7,
  },
  {
    region_id: "reg_008", region_name: "Global Accounts", region_head: "Lisa Thompson",
    capacity_status: "balanced", capacity_risk: "low",
    growth_constraint: "none", capacity_action: "maintain",
    required_headcount: 5, capacity_gap: 0,
    productivity_score: 85.0, pipeline_health_score: 92.0, hiring_efficiency_score: 88.0,
    capacity_composite: 87.9, is_understaffed: false,
    revenue_at_risk_usd: 320000.0,
    capacity_signal: "capacity balanced — 5 reps supporting 6.0M target",
    annual_revenue_target_usd: 6000000.0,
    current_headcount: 5,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const status = searchParams.get("status");
  const risk   = searchParams.get("risk");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-capacity-planning-engine`);
      if (status) url.searchParams.set("status", status);
      if (risk)   url.searchParams.set("risk", risk);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let regions = [...mockRegions];
  if (status) regions = regions.filter((r) => r.capacity_status === status);
  if (risk)   regions = regions.filter((r) => r.capacity_risk === risk);

  const status_counts:     Record<string, number> = {};
  const risk_counts:       Record<string, number> = {};
  const constraint_counts: Record<string, number> = {};
  const action_counts:     Record<string, number> = {};
  let total_comp = 0, total_prod = 0, total_pipe = 0, total_hire = 0, total_risk = 0, total_gap = 0;

  for (const r of mockRegions) {
    status_counts[r.capacity_status]       = (status_counts[r.capacity_status] || 0) + 1;
    risk_counts[r.capacity_risk]           = (risk_counts[r.capacity_risk] || 0) + 1;
    constraint_counts[r.growth_constraint] = (constraint_counts[r.growth_constraint] || 0) + 1;
    action_counts[r.capacity_action]       = (action_counts[r.capacity_action] || 0) + 1;
    total_comp  += r.capacity_composite;
    total_prod  += r.productivity_score;
    total_pipe  += r.pipeline_health_score;
    total_hire  += r.hiring_efficiency_score;
    total_risk  += r.revenue_at_risk_usd;
    if (r.capacity_gap > 0) total_gap += r.capacity_gap;
  }

  const n = mockRegions.length;
  const total_curr = mockRegions.reduce((s, r) => s + r.current_headcount, 0);
  const total_req = mockRegions.reduce((s, r) => s + r.required_headcount, 0);

  return NextResponse.json(sealResponse({
    regions,
    summary: {
      total: n,
      status_counts,
      risk_counts,
      constraint_counts,
      action_counts,
      avg_capacity_composite:       Math.round((total_comp / n) * 10) / 10,
      understaffed_count:           mockRegions.filter((r) => r.is_understaffed).length,
      total_headcount_gap:          total_gap,
      avg_productivity_score:       Math.round((total_prod / n) * 10) / 10,
      avg_pipeline_health_score:    Math.round((total_pipe / n) * 10) / 10,
      avg_hiring_efficiency_score:  Math.round((total_hire / n) * 10) / 10,
      total_revenue_at_risk_usd:    Math.round(total_risk),
      optimal_headcount_range:      `${total_curr}-${total_req}`,
    },
  } as Record<string,unknown>));
}
