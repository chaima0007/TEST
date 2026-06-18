import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    allocation_risk: "low", allocation_pattern: "none",
    allocation_severity: "optimized", recommended_action: "no_action",
    selling_time_score: 0.0, admin_burden_score: 0.0,
    activity_quality_score: 0.0, time_discipline_score: 0.0,
    time_allocation_composite: 0.0,
    has_time_gap: false, requires_allocation_coaching: false,
    estimated_selling_hours_lost_per_week: 0.0,
    allocation_signal: "Time allocation and selling productivity within healthy benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    allocation_risk: "low", allocation_pattern: "none",
    allocation_severity: "optimized", recommended_action: "no_action",
    selling_time_score: 4.0, admin_burden_score: 3.0,
    activity_quality_score: 5.0, time_discipline_score: 4.0,
    time_allocation_composite: 4.0,
    has_time_gap: false, requires_allocation_coaching: false,
    estimated_selling_hours_lost_per_week: 0.0,
    allocation_signal: "Time allocation and selling productivity within healthy benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    allocation_risk: "moderate", allocation_pattern: "time_fragmentation",
    allocation_severity: "developing", recommended_action: "time_audit_coaching",
    selling_time_score: 10.0, admin_burden_score: 8.0,
    activity_quality_score: 18.0, time_discipline_score: 35.0,
    time_allocation_composite: 16.7,
    has_time_gap: false, requires_allocation_coaching: false,
    estimated_selling_hours_lost_per_week: 0.7,
    allocation_signal: "Time fragmentation — 30h customer-facing — composite 17",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    allocation_risk: "moderate", allocation_pattern: "reactive_mode",
    allocation_severity: "developing", recommended_action: "time_audit_coaching",
    selling_time_score: 15.0, admin_burden_score: 14.0,
    activity_quality_score: 32.0, time_discipline_score: 18.0,
    time_allocation_composite: 20.45,
    has_time_gap: false, requires_allocation_coaching: false,
    estimated_selling_hours_lost_per_week: 1.2,
    allocation_signal: "Reactive mode — 28h customer-facing — 20h admin — composite 20",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    allocation_risk: "high", allocation_pattern: "low_selling_time",
    allocation_severity: "burdened", recommended_action: "selling_time_recovery",
    selling_time_score: 38.0, admin_burden_score: 22.0,
    activity_quality_score: 20.0, time_discipline_score: 25.0,
    time_allocation_composite: 28.65,
    has_time_gap: false, requires_allocation_coaching: true,
    estimated_selling_hours_lost_per_week: 2.1,
    allocation_signal: "Low selling time — 22h customer-facing — 28h admin — composite 29",
  },
  {
    rep_id: "rep_006", region: "West",
    allocation_risk: "high", allocation_pattern: "meeting_fatigue",
    allocation_severity: "burdened", recommended_action: "meeting_hygiene_review",
    selling_time_score: 30.0, admin_burden_score: 38.0,
    activity_quality_score: 22.0, time_discipline_score: 30.0,
    time_allocation_composite: 31.3,
    has_time_gap: true, requires_allocation_coaching: true,
    estimated_selling_hours_lost_per_week: 3.5,
    allocation_signal: "Meeting fatigue — 20h customer-facing — 30h admin — 28h internal meetings — composite 31",
  },
  {
    rep_id: "rep_007", region: "APAC",
    allocation_risk: "critical", allocation_pattern: "admin_overload",
    allocation_severity: "fragmented", recommended_action: "admin_reduction_plan",
    selling_time_score: 65.0, admin_burden_score: 60.0,
    activity_quality_score: 55.0, time_discipline_score: 62.0,
    time_allocation_composite: 61.55,
    has_time_gap: true, requires_allocation_coaching: true,
    estimated_selling_hours_lost_per_week: 7.8,
    allocation_signal: "Admin overload — 16h customer-facing — 48h admin — 40h internal meetings — composite 62",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    allocation_risk: "critical", allocation_pattern: "admin_overload",
    allocation_severity: "fragmented", recommended_action: "admin_reduction_plan",
    selling_time_score: 80.0, admin_burden_score: 75.0,
    activity_quality_score: 70.0, time_discipline_score: 72.0,
    time_allocation_composite: 74.95,
    has_time_gap: true, requires_allocation_coaching: true,
    estimated_selling_hours_lost_per_week: 10.4,
    allocation_signal: "Admin overload — 12h customer-facing — 55h admin — 45h internal meetings — composite 75",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-time-allocation-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.allocation_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.allocation_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_sel = 0, total_adm = 0, total_qua = 0, total_dis = 0, total_lost = 0;

  for (const r of mockReps) {
    risk_counts[r.allocation_risk]       = (risk_counts[r.allocation_risk] || 0) + 1;
    pattern_counts[r.allocation_pattern] = (pattern_counts[r.allocation_pattern] || 0) + 1;
    severity_counts[r.allocation_severity] = (severity_counts[r.allocation_severity] || 0) + 1;
    action_counts[r.recommended_action]  = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.time_allocation_composite;
    total_sel  += r.selling_time_score;
    total_adm  += r.admin_burden_score;
    total_qua  += r.activity_quality_score;
    total_dis  += r.time_discipline_score;
    total_lost += r.estimated_selling_hours_lost_per_week;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                                      n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_time_allocation_composite:              Math.round((total_comp / n) * 10) / 10,
      time_gap_count:                             mockReps.filter((r) => r.has_time_gap).length,
      allocation_coaching_count:                  mockReps.filter((r) => r.requires_allocation_coaching).length,
      avg_selling_time_score:                     Math.round((total_sel / n) * 10) / 10,
      avg_admin_burden_score:                     Math.round((total_adm / n) * 10) / 10,
      avg_activity_quality_score:                 Math.round((total_qua / n) * 10) / 10,
      avg_time_discipline_score:                  Math.round((total_dis / n) * 10) / 10,
      total_estimated_selling_hours_lost_per_week: Math.round(total_lost * 100) / 100,
    },
  });
}
