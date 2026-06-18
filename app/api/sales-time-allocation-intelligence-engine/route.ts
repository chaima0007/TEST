import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    time_risk: "low", time_pattern: "none",
    time_severity: "optimized", recommended_action: "no_action",
    priority_allocation_score: 0.0, balance_score: 0.0,
    pipeline_focus_score: 0.0, selling_effectiveness_score: 0.0,
    time_composite: 0.0,
    has_time_gap: false, requires_time_coaching: false,
    estimated_quota_risk_usd: 0.0,
    time_signal: "Time allocation optimized — priority accounts, pipeline building, and selling hours within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    time_risk: "low", time_pattern: "none",
    time_severity: "optimized", recommended_action: "no_action",
    priority_allocation_score: 4.0, balance_score: 3.0,
    pipeline_focus_score: 5.0, selling_effectiveness_score: 2.0,
    time_composite: 3.65,
    has_time_gap: false, requires_time_coaching: true,
    estimated_quota_risk_usd: 0.0,
    time_signal: "Time allocation optimized — priority accounts, pipeline building, and selling hours within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    time_risk: "moderate", time_pattern: "renewal_hover",
    time_severity: "balanced", recommended_action: "account_prioritization_coaching",
    priority_allocation_score: 22.0, balance_score: 18.0,
    pipeline_focus_score: 20.0, selling_effectiveness_score: 15.0,
    time_composite: 19.55,
    has_time_gap: true, requires_time_coaching: true,
    estimated_quota_risk_usd: 198000.0,
    time_signal: "Renewal hover — 48% time on high-priority accounts — 18% on admin — 35% reactive — composite 20",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    time_risk: "moderate", time_pattern: "wrong_size_focus",
    time_severity: "balanced", recommended_action: "account_prioritization_coaching",
    priority_allocation_score: 20.0, balance_score: 22.0,
    pipeline_focus_score: 18.0, selling_effectiveness_score: 20.0,
    time_composite: 20.3,
    has_time_gap: true, requires_time_coaching: true,
    estimated_quota_risk_usd: 312000.0,
    time_signal: "Wrong-size focus — 42% time on high-priority accounts — 22% on admin — 42% reactive — composite 20",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    time_risk: "high", time_pattern: "reactive_time_sink",
    time_severity: "misaligned", recommended_action: "pipeline_focus_coaching",
    priority_allocation_score: 40.0, balance_score: 45.0,
    pipeline_focus_score: 38.0, selling_effectiveness_score: 30.0,
    time_composite: 39.25,
    has_time_gap: true, requires_time_coaching: true,
    estimated_quota_risk_usd: 756000.0,
    time_signal: "Reactive time sink — 30% time on high-priority accounts — 28% on admin — 68% reactive — composite 39",
  },
  {
    rep_id: "rep_006", region: "West",
    time_risk: "high", time_pattern: "admin_overload",
    time_severity: "misaligned", recommended_action: "admin_reduction_coaching",
    priority_allocation_score: 48.0, balance_score: 52.0,
    pipeline_focus_score: 40.0, selling_effectiveness_score: 45.0,
    time_composite: 46.7,
    has_time_gap: true, requires_time_coaching: true,
    estimated_quota_risk_usd: 1404000.0,
    time_signal: "Admin overload — 25% time on high-priority accounts — 38% on admin — 58% reactive — composite 47",
  },
  {
    rep_id: "rep_007", region: "APAC",
    time_risk: "critical", time_pattern: "high_priority_neglect",
    time_severity: "scattered", recommended_action: "time_strategy_reset",
    priority_allocation_score: 72.0, balance_score: 68.0,
    pipeline_focus_score: 65.0, selling_effectiveness_score: 72.0,
    time_composite: 69.55,
    has_time_gap: true, requires_time_coaching: true,
    estimated_quota_risk_usd: 2574000.0,
    time_signal: "High-priority neglect — 15% time on high-priority accounts — 35% on admin — 72% reactive — composite 70",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    time_risk: "critical", time_pattern: "high_priority_neglect",
    time_severity: "scattered", recommended_action: "time_strategy_reset",
    priority_allocation_score: 100.0, balance_score: 100.0,
    pipeline_focus_score: 100.0, selling_effectiveness_score: 100.0,
    time_composite: 100.0,
    has_time_gap: true, requires_time_coaching: true,
    estimated_quota_risk_usd: 4950000.0,
    time_signal: "High-priority neglect — 10% time on high-priority accounts — 40% on admin — 75% reactive — composite 100",
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
  if (risk)    reps = reps.filter((r) => r.time_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.time_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_pa = 0, total_ba = 0, total_pf = 0, total_se = 0, total_qr = 0;

  for (const r of mockReps) {
    risk_counts[r.time_risk]         = (risk_counts[r.time_risk] || 0) + 1;
    pattern_counts[r.time_pattern]   = (pattern_counts[r.time_pattern] || 0) + 1;
    severity_counts[r.time_severity] = (severity_counts[r.time_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.time_composite;
    total_pa   += r.priority_allocation_score;
    total_ba   += r.balance_score;
    total_pf   += r.pipeline_focus_score;
    total_se   += r.selling_effectiveness_score;
    total_qr   += r.estimated_quota_risk_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                              n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_time_composite:                 Math.round((total_comp / n) * 10) / 10,
      time_gap_count:                     mockReps.filter((r) => r.has_time_gap).length,
      coaching_count:                     mockReps.filter((r) => r.requires_time_coaching).length,
      avg_priority_allocation_score:      Math.round((total_pa / n) * 10) / 10,
      avg_balance_score:                  Math.round((total_ba / n) * 10) / 10,
      avg_pipeline_focus_score:           Math.round((total_pf / n) * 10) / 10,
      avg_selling_effectiveness_score:    Math.round((total_se / n) * 10) / 10,
      total_estimated_quota_risk_usd:     Math.round(total_qr * 100) / 100,
    },
  });
}
