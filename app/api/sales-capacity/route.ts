import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockTeams = [
  {
    team_id: "t_001",
    region: "EMEA",
    segment: "enterprise",
    manager_id: "mgr_001",
    capacity_status: "under_capacity",
    hiring_urgency: "monitor",
    capacity_health: "constrained",
    capacity_action: "strategic_review",
    effective_capacity_pct: 79.9,
    headcount_gap: 0,
    quota_at_risk: 1005000,
    pipeline_per_rep: 1500000,
    required_attainment: 100.0,
    ramp_impact: 10.0,
    productivity_index: 80.75,
    is_capacity_constrained: true,
    needs_immediate_hire: false,
    current_reps: 10,
    target_reps: 10,
    total_team_quota: 5000000,
    pipeline_coverage_ratio: 3.0,
  },
  {
    team_id: "t_002",
    region: "NAMER",
    segment: "enterprise",
    manager_id: "mgr_002",
    capacity_status: "critical_shortage",
    hiring_urgency: "immediate",
    capacity_health: "critical",
    capacity_action: "hire_immediately",
    effective_capacity_pct: 42.0,
    headcount_gap: 4,
    quota_at_risk: 3480000,
    pipeline_per_rep: 900000,
    required_attainment: 150.0,
    ramp_impact: 16.7,
    productivity_index: 61.5,
    is_capacity_constrained: true,
    needs_immediate_hire: true,
    current_reps: 6,
    target_reps: 10,
    total_team_quota: 6000000,
    pipeline_coverage_ratio: 2.5,
  },
  {
    team_id: "t_003",
    region: "APAC",
    segment: "mid_market",
    manager_id: "mgr_003",
    capacity_status: "at_capacity",
    hiring_urgency: "monitor",
    capacity_health: "healthy",
    capacity_action: "maintain_capacity",
    effective_capacity_pct: 91.0,
    headcount_gap: 0,
    quota_at_risk: 270000,
    pipeline_per_rep: 600000,
    required_attainment: 100.0,
    ramp_impact: 0.0,
    productivity_index: 88.0,
    is_capacity_constrained: false,
    needs_immediate_hire: false,
    current_reps: 8,
    target_reps: 8,
    total_team_quota: 2400000,
    pipeline_coverage_ratio: 2.5,
  },
  {
    team_id: "t_004",
    region: "EMEA",
    segment: "mid_market",
    manager_id: "mgr_001",
    capacity_status: "over_capacity",
    hiring_urgency: "monitor",
    capacity_health: "healthy",
    capacity_action: "maintain_capacity",
    effective_capacity_pct: 112.0,
    headcount_gap: 0,
    quota_at_risk: 0,
    pipeline_per_rep: 720000,
    required_attainment: 88.0,
    ramp_impact: 8.3,
    productivity_index: 91.0,
    is_capacity_constrained: false,
    needs_immediate_hire: false,
    current_reps: 12,
    target_reps: 10,
    total_team_quota: 3600000,
    pipeline_coverage_ratio: 2.4,
  },
  {
    team_id: "t_005",
    region: "LATAM",
    segment: "smb",
    manager_id: "mgr_004",
    capacity_status: "under_capacity",
    hiring_urgency: "near_term",
    capacity_health: "constrained",
    capacity_action: "redistribute_quota",
    effective_capacity_pct: 63.0,
    headcount_gap: 3,
    quota_at_risk: 925000,
    pipeline_per_rep: 350000,
    required_attainment: 119.0,
    ramp_impact: 14.3,
    productivity_index: 69.5,
    is_capacity_constrained: true,
    needs_immediate_hire: false,
    current_reps: 7,
    target_reps: 10,
    total_team_quota: 2500000,
    pipeline_coverage_ratio: 1.4,
  },
  {
    team_id: "t_006",
    region: "NAMER",
    segment: "mid_market",
    manager_id: "mgr_002",
    capacity_status: "at_capacity",
    hiring_urgency: "planned",
    capacity_health: "at_risk",
    capacity_action: "focus_productivity",
    effective_capacity_pct: 82.5,
    headcount_gap: 1,
    quota_at_risk: 437500,
    pipeline_per_rep: 750000,
    required_attainment: 103.0,
    ramp_impact: 25.0,
    productivity_index: 62.0,
    is_capacity_constrained: false,
    needs_immediate_hire: false,
    current_reps: 8,
    target_reps: 9,
    total_team_quota: 3200000,
    pipeline_coverage_ratio: 2.2,
  },
  {
    team_id: "t_007",
    region: "APAC",
    segment: "enterprise",
    manager_id: "mgr_003",
    capacity_status: "under_capacity",
    hiring_urgency: "near_term",
    capacity_health: "constrained",
    capacity_action: "accelerate_ramp",
    effective_capacity_pct: 65.5,
    headcount_gap: 2,
    quota_at_risk: 1552500,
    pipeline_per_rep: 1350000,
    required_attainment: 115.4,
    ramp_impact: 53.3,
    productivity_index: 58.5,
    is_capacity_constrained: true,
    needs_immediate_hire: false,
    current_reps: 5,
    target_reps: 7,
    total_team_quota: 4500000,
    pipeline_coverage_ratio: 3.0,
  },
  {
    team_id: "t_008",
    region: "EMEA",
    segment: "smb",
    manager_id: "mgr_005",
    capacity_status: "at_capacity",
    hiring_urgency: "monitor",
    capacity_health: "healthy",
    capacity_action: "maintain_capacity",
    effective_capacity_pct: 85.0,
    headcount_gap: 0,
    quota_at_risk: 180000,
    pipeline_per_rep: 200000,
    required_attainment: 100.0,
    ramp_impact: 0.0,
    productivity_index: 85.0,
    is_capacity_constrained: false,
    needs_immediate_hire: false,
    current_reps: 6,
    target_reps: 6,
    total_team_quota: 1200000,
    pipeline_coverage_ratio: 1.5,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const status  = searchParams.get("status");
  const urgency = searchParams.get("urgency");
  const region  = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-capacity`);
      if (status)  url.searchParams.set("status", status);
      if (urgency) url.searchParams.set("urgency", urgency);
      if (region)  url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let teams = [...mockTeams];
  if (status)  teams = teams.filter((t) => t.capacity_status === status);
  if (urgency) teams = teams.filter((t) => t.hiring_urgency === urgency);
  if (region)  teams = teams.filter((t) => t.region === region);

  const status_counts:  Record<string, number> = {};
  const urgency_counts: Record<string, number> = {};
  const action_counts:  Record<string, number> = {};
  let total_cap = 0, total_quota_risk = 0, total_prod = 0;

  for (const t of mockTeams) {
    status_counts[t.capacity_status]   = (status_counts[t.capacity_status] || 0) + 1;
    urgency_counts[t.hiring_urgency]   = (urgency_counts[t.hiring_urgency] || 0) + 1;
    action_counts[t.capacity_action]   = (action_counts[t.capacity_action] || 0) + 1;
    total_cap        += t.effective_capacity_pct;
    total_quota_risk += t.quota_at_risk;
    total_prod       += t.productivity_index;
  }

  const n = mockTeams.length;

  return NextResponse.json({
    teams,
    summary: {
      total:                   n,
      status_counts,
      urgency_counts,
      action_counts,
      avg_effective_capacity:  Math.round((total_cap / n) * 10) / 10,
      total_quota_at_risk:     Math.round(total_quota_risk * 100) / 100,
      avg_productivity_index:  Math.round((total_prod / n) * 10) / 10,
      constrained_count:       mockTeams.filter((t) => t.is_capacity_constrained).length,
      immediate_hire_count:    mockTeams.filter((t) => t.needs_immediate_hire).length,
      critical_count:          mockTeams.filter((t) => t.capacity_health === "critical").length,
      total_headcount_gap:     mockTeams.reduce((s, t) => s + t.headcount_gap, 0),
    },
  });
}
