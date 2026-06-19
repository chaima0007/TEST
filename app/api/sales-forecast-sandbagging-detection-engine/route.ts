import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    sandbagging_risk: "low", sandbagging_pattern: "none",
    sandbagging_severity: "accurate", recommended_action: "no_action",
    commit_accuracy_score: 0.0, upside_manipulation_score: 0.0,
    deal_timing_score: 0.0, pattern_consistency_score: 0.0,
    sandbagging_composite: 0.0, is_sandbagging: false, requires_intervention: false,
    estimated_hidden_revenue_usd: 0.0,
    sandbagging_signal: "Forecast accuracy within expected variance — no sandbagging signals",
  },
  {
    rep_id: "rep_002", region: "East",
    sandbagging_risk: "low", sandbagging_pattern: "consistent_upside",
    sandbagging_severity: "watch", recommended_action: "forecast_coaching",
    commit_accuracy_score: 14.0, upside_manipulation_score: 15.0,
    deal_timing_score: 6.0, pattern_consistency_score: 5.0,
    sandbagging_composite: 11.5, is_sandbagging: false, requires_intervention: false,
    estimated_hidden_revenue_usd: 5750.0,
    sandbagging_signal: "Consistent upside — 18% over commit — 2 consecutive upside periods — composite 12",
  },
  {
    rep_id: "rep_003", region: "Central",
    sandbagging_risk: "moderate", sandbagging_pattern: "consistent_upside",
    sandbagging_severity: "watch", recommended_action: "pipeline_review",
    commit_accuracy_score: 28.0, upside_manipulation_score: 28.0,
    deal_timing_score: 10.0, pattern_consistency_score: 15.0,
    sandbagging_composite: 22.3, is_sandbagging: false, requires_intervention: false,
    estimated_hidden_revenue_usd: 22300.0,
    sandbagging_signal: "Consistent upside — 35% over commit — 3 consecutive upside periods — composite 22",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    sandbagging_risk: "moderate", sandbagging_pattern: "commit_minimization",
    sandbagging_severity: "watch", recommended_action: "pipeline_review",
    commit_accuracy_score: 35.0, upside_manipulation_score: 20.0,
    deal_timing_score: 12.0, pattern_consistency_score: 10.0,
    sandbagging_composite: 23.7, is_sandbagging: false, requires_intervention: false,
    estimated_hidden_revenue_usd: 35550.0,
    sandbagging_signal: "Commit minimization — 28% over commit — 4 late-stage deals withheld — composite 24",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    sandbagging_risk: "high", sandbagging_pattern: "deal_timing_manipulation",
    sandbagging_severity: "suspected", recommended_action: "comp_plan_review",
    commit_accuracy_score: 42.0, upside_manipulation_score: 35.0,
    deal_timing_score: 45.0, pattern_consistency_score: 20.0,
    sandbagging_composite: 38.0, is_sandbagging: false, requires_intervention: true,
    estimated_hidden_revenue_usd: 76000.0,
    sandbagging_signal: "Deal timing manipulation — 3 deals pulled from Q+1 — 2 intentional slips — composite 38",
  },
  {
    rep_id: "rep_006", region: "West",
    sandbagging_risk: "high", sandbagging_pattern: "forecast_sandbagging",
    sandbagging_severity: "suspected", recommended_action: "comp_plan_review",
    commit_accuracy_score: 50.0, upside_manipulation_score: 45.0,
    deal_timing_score: 30.0, pattern_consistency_score: 25.0,
    sandbagging_composite: 41.3, is_sandbagging: true, requires_intervention: true,
    estimated_hidden_revenue_usd: 103250.0,
    sandbagging_signal: "Forecast sandbagging — 52% over commit — 4 consecutive upside periods — 3 late-stage deals withheld — composite 41",
  },
  {
    rep_id: "rep_007", region: "APAC",
    sandbagging_risk: "critical", sandbagging_pattern: "forecast_sandbagging",
    sandbagging_severity: "confirmed", recommended_action: "executive_confrontation",
    commit_accuracy_score: 70.0, upside_manipulation_score: 68.0,
    deal_timing_score: 55.0, pattern_consistency_score: 50.0,
    sandbagging_composite: 63.9, is_sandbagging: true, requires_intervention: true,
    estimated_hidden_revenue_usd: 191700.0,
    sandbagging_signal: "Forecast sandbagging — 80% over commit — 5 consecutive upside periods — 5 deals pulled from Q+1 — composite 64",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    sandbagging_risk: "critical", sandbagging_pattern: "forecast_sandbagging",
    sandbagging_severity: "confirmed", recommended_action: "executive_confrontation",
    commit_accuracy_score: 80.0, upside_manipulation_score: 75.0,
    deal_timing_score: 65.0, pattern_consistency_score: 60.0,
    sandbagging_composite: 73.3, is_sandbagging: true, requires_intervention: true,
    estimated_hidden_revenue_usd: 293200.0,
    sandbagging_signal: "Forecast sandbagging — 120% over commit — 6 consecutive upside periods — 4 intentional slips — composite 73",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-forecast-sandbagging-detection-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.sandbagging_risk     === risk);
  if (pattern) reps = reps.filter((r) => r.sandbagging_pattern  === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_c = 0, total_u = 0, total_t = 0, total_p = 0, total_rev = 0;

  for (const r of mockReps) {
    risk_counts[r.sandbagging_risk]      = (risk_counts[r.sandbagging_risk] || 0) + 1;
    pattern_counts[r.sandbagging_pattern] = (pattern_counts[r.sandbagging_pattern] || 0) + 1;
    severity_counts[r.sandbagging_severity] = (severity_counts[r.sandbagging_severity] || 0) + 1;
    action_counts[r.recommended_action]  = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.sandbagging_composite;
    total_c    += r.commit_accuracy_score;
    total_u    += r.upside_manipulation_score;
    total_t    += r.deal_timing_score;
    total_p    += r.pattern_consistency_score;
    total_rev  += r.estimated_hidden_revenue_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                                n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_sandbagging_composite:            Math.round((total_comp / n) * 10) / 10,
      sandbagging_count:                    mockReps.filter((r) => r.is_sandbagging).length,
      intervention_count:                   mockReps.filter((r) => r.requires_intervention).length,
      avg_commit_accuracy_score:            Math.round((total_c / n) * 10) / 10,
      avg_upside_manipulation_score:        Math.round((total_u / n) * 10) / 10,
      avg_deal_timing_score:                Math.round((total_t / n) * 10) / 10,
      avg_pattern_consistency_score:        Math.round((total_p / n) * 10) / 10,
      total_estimated_hidden_revenue_usd:   Math.round(total_rev * 100) / 100,
    },
  });
}
