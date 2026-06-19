import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", rep_name: "Maya Rodriguez", region: "West",
    burnout_risk: "none", burnout_stage: "engaged",
    primary_burnout_signal: "none", burnout_action: "monitor",
    activity_health_score: 95.0, wellbeing_score: 91.0,
    performance_sustainability_score: 88.0, social_engagement_score: 89.0,
    burnout_composite: 5.3, is_at_burnout_risk: false, needs_immediate_support: false,
    estimated_productivity_impact_pct: 0.0,
    burnout_signal: "rep healthy — no burnout signals detected",
  },
  {
    rep_id: "rep_002", rep_name: "James Park", region: "East",
    burnout_risk: "early_warning", burnout_stage: "coasting",
    primary_burnout_signal: "activity_decline", burnout_action: "check_in",
    activity_health_score: 72.0, wellbeing_score: 68.0,
    performance_sustainability_score: 74.0, social_engagement_score: 70.0,
    burnout_composite: 28.4, is_at_burnout_risk: false, needs_immediate_support: false,
    estimated_productivity_impact_pct: 8.5,
    burnout_signal: "activity down 18% — 3 weeks without a close",
  },
  {
    rep_id: "rep_003", rep_name: "Sarah Chen", region: "Central",
    burnout_risk: "moderate", burnout_stage: "disengaging",
    primary_burnout_signal: "exhaustion", burnout_action: "coaching_session",
    activity_health_score: 58.0, wellbeing_score: 52.0,
    performance_sustainability_score: 61.0, social_engagement_score: 64.0,
    burnout_composite: 41.8, is_at_burnout_risk: true, needs_immediate_support: false,
    estimated_productivity_impact_pct: 20.9,
    burnout_signal: "4 sick days in 90d, only 3 PTO days used",
  },
  {
    rep_id: "rep_004", rep_name: "Alex Okonkwo", region: "West",
    burnout_risk: "high", burnout_stage: "burned_out",
    primary_burnout_signal: "performance_decay", burnout_action: "workload_reduction",
    activity_health_score: 40.0, wellbeing_score: 36.0,
    performance_sustainability_score: 32.0, social_engagement_score: 45.0,
    burnout_composite: 62.1, is_at_burnout_risk: true, needs_immediate_support: true,
    estimated_productivity_impact_pct: 43.5,
    burnout_signal: "win rate declined 18pts — customer escalations: 4",
  },
  {
    rep_id: "rep_005", rep_name: "Emma Thompson", region: "Northeast",
    burnout_risk: "critical", burnout_stage: "depleted",
    primary_burnout_signal: "overwhelm", burnout_action: "urgent_intervention",
    activity_health_score: 22.0, wellbeing_score: 18.0,
    performance_sustainability_score: 24.0, social_engagement_score: 28.0,
    burnout_composite: 77.6, is_at_burnout_risk: true, needs_immediate_support: true,
    estimated_productivity_impact_pct: 54.3,
    burnout_signal: "chronic overwork — 25h overtime/wk + 12h weekends",
  },
  {
    rep_id: "rep_006", rep_name: "Carlos Mendez", region: "Southeast",
    burnout_risk: "early_warning", burnout_stage: "coasting",
    primary_burnout_signal: "isolation", burnout_action: "check_in",
    activity_health_score: 69.0, wellbeing_score: 74.0,
    performance_sustainability_score: 71.0, social_engagement_score: 48.0,
    burnout_composite: 31.2, is_at_burnout_risk: false, needs_immediate_support: false,
    estimated_productivity_impact_pct: 9.4,
    burnout_signal: "peer score 42/100, manager check-ins 0.5x/mo",
  },
  {
    rep_id: "rep_007", rep_name: "Lisa Tanaka", region: "Northwest",
    burnout_risk: "moderate", burnout_stage: "disengaging",
    primary_burnout_signal: "activity_decline", burnout_action: "coaching_session",
    activity_health_score: 55.0, wellbeing_score: 60.0,
    performance_sustainability_score: 58.0, social_engagement_score: 62.0,
    burnout_composite: 42.9, is_at_burnout_risk: true, needs_immediate_support: false,
    estimated_productivity_impact_pct: 21.5,
    burnout_signal: "activity down 28% — 5 weeks without a close",
  },
  {
    rep_id: "rep_008", rep_name: "David Singh", region: "Southwest",
    burnout_risk: "none", burnout_stage: "engaged",
    primary_burnout_signal: "none", burnout_action: "monitor",
    activity_health_score: 92.0, wellbeing_score: 88.0,
    performance_sustainability_score: 85.0, social_engagement_score: 91.0,
    burnout_composite: 8.1, is_at_burnout_risk: false, needs_immediate_support: false,
    estimated_productivity_impact_pct: 0.0,
    burnout_signal: "rep healthy — no burnout signals detected",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk  = searchParams.get("risk");
  const stage = searchParams.get("stage");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-burnout-risk-engine`);
      if (risk)  url.searchParams.set("risk",  risk);
      if (stage) url.searchParams.set("stage", stage);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)  reps = reps.filter((r) => r.burnout_risk === risk);
  if (stage) reps = reps.filter((r) => r.burnout_stage === stage);

  const risk_counts:   Record<string, number> = {};
  const stage_counts:  Record<string, number> = {};
  const signal_counts: Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  let total_composite = 0, total_activity = 0, total_wellbeing = 0, total_perf = 0, total_social = 0, total_impact = 0;

  for (const r of mockReps) {
    risk_counts[r.burnout_risk]                = (risk_counts[r.burnout_risk] || 0) + 1;
    stage_counts[r.burnout_stage]              = (stage_counts[r.burnout_stage] || 0) + 1;
    signal_counts[r.primary_burnout_signal]    = (signal_counts[r.primary_burnout_signal] || 0) + 1;
    action_counts[r.burnout_action]            = (action_counts[r.burnout_action] || 0) + 1;
    total_composite += r.burnout_composite;
    total_activity  += r.activity_health_score;
    total_wellbeing += r.wellbeing_score;
    total_perf      += r.performance_sustainability_score;
    total_social    += r.social_engagement_score;
    total_impact    += r.estimated_productivity_impact_pct;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                              n,
      risk_counts,
      stage_counts,
      signal_counts,
      action_counts,
      avg_burnout_composite:              Math.round((total_composite / n) * 10) / 10,
      at_burnout_risk_count:              mockReps.filter((r) => r.is_at_burnout_risk).length,
      immediate_support_count:            mockReps.filter((r) => r.needs_immediate_support).length,
      avg_activity_health_score:          Math.round((total_activity  / n) * 10) / 10,
      avg_wellbeing_score:                Math.round((total_wellbeing / n) * 10) / 10,
      avg_performance_sustainability_score: Math.round((total_perf   / n) * 10) / 10,
      avg_social_engagement_score:        Math.round((total_social   / n) * 10) / 10,
      total_productivity_impact_pct:      Math.round(total_impact * 10) / 10,
    },
  });
}
