import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sales-rep-burnout] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", rep_name: "Alice Dupont",
    region: "EMEA", manager_id: "mgr_001",
    burnout_risk: "building", burnout_category: "stressed",
    burnout_pattern: "declining", burnout_action: "coaching",
    overwork_score: 0.0, disengagement_score: 60.2,
    performance_decline_score: 53.6, wellbeing_score: 38.0,
    burnout_composite_score: 40.8, predicted_turnover_probability: 45.6,
    intervention_urgency_score: 42.4,
    is_at_risk: false, needs_immediate_action: false,
    deals_closed_this_quarter: 6, deals_closed_last_quarter: 9,
    win_rate_current: 38.0, win_rate_prev_quarter: 52.0,
  },
  {
    rep_id: "rep_002", rep_name: "Marco Rossi",
    region: "EMEA", manager_id: "mgr_001",
    burnout_risk: "critical", burnout_category: "burned_out",
    burnout_pattern: "overworking", burnout_action: "immediate_intervention",
    overwork_score: 82.4, disengagement_score: 12.4,
    performance_decline_score: 68.2, wellbeing_score: 22.0,
    burnout_composite_score: 76.4, predicted_turnover_probability: 82.5,
    intervention_urgency_score: 84.3,
    is_at_risk: true, needs_immediate_action: true,
    deals_closed_this_quarter: 14, deals_closed_last_quarter: 10,
    win_rate_current: 42.0, win_rate_prev_quarter: 58.0,
  },
  {
    rep_id: "rep_003", rep_name: "Sarah Kim",
    region: "APAC", manager_id: "mgr_002",
    burnout_risk: "minimal", burnout_category: "healthy",
    burnout_pattern: "stable", burnout_action: "monitor",
    overwork_score: 8.2, disengagement_score: 6.4,
    performance_decline_score: 12.1, wellbeing_score: 72.0,
    burnout_composite_score: 12.8, predicted_turnover_probability: 14.2,
    intervention_urgency_score: 13.1,
    is_at_risk: false, needs_immediate_action: false,
    deals_closed_this_quarter: 11, deals_closed_last_quarter: 10,
    win_rate_current: 62.0, win_rate_prev_quarter: 60.0,
  },
  {
    rep_id: "rep_004", rep_name: "Carlos Mendez",
    region: "LATAM", manager_id: "mgr_003",
    burnout_risk: "high", burnout_category: "overloaded",
    burnout_pattern: "overworking", burnout_action: "workload_review",
    overwork_score: 64.8, disengagement_score: 24.2,
    performance_decline_score: 28.6, wellbeing_score: 30.0,
    burnout_composite_score: 56.2, predicted_turnover_probability: 62.4,
    intervention_urgency_score: 60.5,
    is_at_risk: true, needs_immediate_action: false,
    deals_closed_this_quarter: 12, deals_closed_last_quarter: 11,
    win_rate_current: 54.0, win_rate_prev_quarter: 58.0,
  },
  {
    rep_id: "rep_005", rep_name: "Nina Petrov",
    region: "EMEA", manager_id: "mgr_001",
    burnout_risk: "building", burnout_category: "stressed",
    burnout_pattern: "disengaging", burnout_action: "coaching",
    overwork_score: 18.4, disengagement_score: 52.6,
    performance_decline_score: 24.8, wellbeing_score: 48.0,
    burnout_composite_score: 34.6, predicted_turnover_probability: 38.2,
    intervention_urgency_score: 35.8,
    is_at_risk: false, needs_immediate_action: false,
    deals_closed_this_quarter: 7, deals_closed_last_quarter: 8,
    win_rate_current: 48.0, win_rate_prev_quarter: 52.0,
  },
  {
    rep_id: "rep_006", rep_name: "James Okonkwo",
    region: "MEA", manager_id: "mgr_004",
    burnout_risk: "minimal", burnout_category: "healthy",
    burnout_pattern: "stable", burnout_action: "monitor",
    overwork_score: 4.2, disengagement_score: 8.6,
    performance_decline_score: 4.8, wellbeing_score: 78.0,
    burnout_composite_score: 8.4, predicted_turnover_probability: 9.8,
    intervention_urgency_score: 8.8,
    is_at_risk: false, needs_immediate_action: false,
    deals_closed_this_quarter: 9, deals_closed_last_quarter: 9,
    win_rate_current: 68.0, win_rate_prev_quarter: 66.0,
  },
  {
    rep_id: "rep_007", rep_name: "Yuki Tanaka",
    region: "APAC", manager_id: "mgr_002",
    burnout_risk: "high", burnout_category: "stressed",
    burnout_pattern: "declining", burnout_action: "coaching",
    overwork_score: 22.4, disengagement_score: 38.6,
    performance_decline_score: 58.4, wellbeing_score: 40.0,
    burnout_composite_score: 52.4, predicted_turnover_probability: 58.6,
    intervention_urgency_score: 54.8,
    is_at_risk: true, needs_immediate_action: false,
    deals_closed_this_quarter: 5, deals_closed_last_quarter: 9,
    win_rate_current: 35.0, win_rate_prev_quarter: 55.0,
  },
  {
    rep_id: "rep_008", rep_name: "Emma Wilson",
    region: "NAMER", manager_id: "mgr_005",
    burnout_risk: "building", burnout_category: "stressed",
    burnout_pattern: "disengaging", burnout_action: "coaching",
    overwork_score: 12.6, disengagement_score: 46.8,
    performance_decline_score: 18.4, wellbeing_score: 44.0,
    burnout_composite_score: 28.4, predicted_turnover_probability: 32.6,
    intervention_urgency_score: 29.8,
    is_at_risk: false, needs_immediate_action: false,
    deals_closed_this_quarter: 8, deals_closed_last_quarter: 9,
    win_rate_current: 50.0, win_rate_prev_quarter: 54.0,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk     = searchParams.get("risk");
  const category = searchParams.get("category");
  const region   = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-rep-burnout`);
      if (risk)     url.searchParams.set("risk", risk);
      if (category) url.searchParams.set("category", category);
      if (region)   url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)     reps = reps.filter((r) => r.burnout_risk === risk);
  if (category) reps = reps.filter((r) => r.burnout_category === category);
  if (region)   reps = reps.filter((r) => r.region === region);

  const risk_counts:     Record<string, number> = {};
  const category_counts: Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_composite = 0, total_turnover = 0, total_overwork = 0,
      total_disengage = 0, total_perf_dec = 0, total_wellbeing = 0;

  for (const r of mockReps) {
    risk_counts[r.burnout_risk]       = (risk_counts[r.burnout_risk] || 0) + 1;
    category_counts[r.burnout_category] = (category_counts[r.burnout_category] || 0) + 1;
    pattern_counts[r.burnout_pattern] = (pattern_counts[r.burnout_pattern] || 0) + 1;
    action_counts[r.burnout_action]   = (action_counts[r.burnout_action] || 0) + 1;
    total_composite += r.burnout_composite_score;
    total_turnover  += r.predicted_turnover_probability;
    total_overwork  += r.overwork_score;
    total_disengage += r.disengagement_score;
    total_perf_dec  += r.performance_decline_score;
    total_wellbeing += r.wellbeing_score;
  }

  const n = mockReps.length;

  return sealResponse(NextResponse.json({
    reps,
    summary: {
      total:                              n,
      risk_counts,
      category_counts,
      pattern_counts,
      action_counts,
      avg_burnout_composite_score:        Math.round((total_composite / n) * 10) / 10,
      avg_predicted_turnover_probability: Math.round((total_turnover / n) * 10) / 10,
      at_risk_count:                      mockReps.filter((r) => r.is_at_risk).length,
      immediate_action_count:             mockReps.filter((r) => r.needs_immediate_action).length,
      avg_overwork_score:                 Math.round((total_overwork / n) * 10) / 10,
      avg_disengagement_score:            Math.round((total_disengage / n) * 10) / 10,
      avg_performance_decline_score:      Math.round((total_perf_dec / n) * 10) / 10,
      avg_wellbeing_score:                Math.round((total_wellbeing / n) * 10) / 10,
    },
  }));
}
