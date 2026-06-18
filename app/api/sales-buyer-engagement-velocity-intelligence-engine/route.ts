import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    engagement_risk: "low", engagement_pattern: "none",
    engagement_severity: "accelerating", recommended_action: "no_action",
    velocity_score: 0.0, breadth_score: 0.0,
    responsiveness_score: 0.0, momentum_score: 0.0,
    engagement_composite: 0.0,
    has_engagement_gap: false, requires_engagement_coaching: false,
    estimated_pipeline_at_risk_usd: 0.0,
    engagement_signal: "Buyer engagement healthy — response velocity, stakeholder breadth, and deal momentum within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    engagement_risk: "low", engagement_pattern: "none",
    engagement_severity: "accelerating", recommended_action: "no_action",
    velocity_score: 4.0, breadth_score: 3.0,
    responsiveness_score: 5.0, momentum_score: 2.0,
    engagement_composite: 3.65,
    has_engagement_gap: false, requires_engagement_coaching: false,
    estimated_pipeline_at_risk_usd: 0.0,
    engagement_signal: "Buyer engagement healthy — response velocity, stakeholder breadth, and deal momentum within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    engagement_risk: "moderate", engagement_pattern: "momentum_reversal",
    engagement_severity: "engaged", recommended_action: "re_engagement_sequence_coaching",
    velocity_score: 20.0, breadth_score: 18.0,
    responsiveness_score: 22.0, momentum_score: 15.0,
    engagement_composite: 19.25,
    has_engagement_gap: false, requires_engagement_coaching: true,
    estimated_pipeline_at_risk_usd: 48000.0,
    engagement_signal: "Momentum reversal — 2.8d avg buyer response time — 3.2 avg stakeholders — 0.8 ghosting episodes/deal — composite 19",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    engagement_risk: "moderate", engagement_pattern: "response_lag_accumulation",
    engagement_severity: "engaged", recommended_action: "re_engagement_sequence_coaching",
    velocity_score: 25.0, breadth_score: 20.0,
    responsiveness_score: 22.0, momentum_score: 18.0,
    engagement_composite: 21.85,
    has_engagement_gap: false, requires_engagement_coaching: true,
    estimated_pipeline_at_risk_usd: 96000.0,
    engagement_signal: "Response lag accumulation — 3.5d avg buyer response time — 2.8 avg stakeholders — 1.2 ghosting episodes/deal — composite 22",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    engagement_risk: "high", engagement_pattern: "single_contact_dependency",
    engagement_severity: "slowing", recommended_action: "multithreading_coaching",
    velocity_score: 40.0, breadth_score: 45.0,
    responsiveness_score: 38.0, momentum_score: 30.0,
    engagement_composite: 39.35,
    has_engagement_gap: false, requires_engagement_coaching: true,
    estimated_pipeline_at_risk_usd: 228000.0,
    engagement_signal: "Single contact dependency — 4.5d avg buyer response time — 1.8 avg stakeholders — 1.8 ghosting episodes/deal — composite 39",
  },
  {
    rep_id: "rep_006", region: "West",
    engagement_risk: "high", engagement_pattern: "buyer_ghosting_cycle",
    engagement_severity: "slowing", recommended_action: "deal_velocity_coaching",
    velocity_score: 55.0, breadth_score: 42.0,
    responsiveness_score: 48.0, momentum_score: 52.0,
    engagement_composite: 50.05,
    has_engagement_gap: true, requires_engagement_coaching: true,
    estimated_pipeline_at_risk_usd: 540000.0,
    engagement_signal: "Buyer ghosting cycle — 5.5d avg buyer response time — 1.5 avg stakeholders — 2.8 ghosting episodes/deal — composite 50",
  },
  {
    rep_id: "rep_007", region: "APAC",
    engagement_risk: "critical", engagement_pattern: "executive_access_deficit",
    engagement_severity: "stalled", recommended_action: "executive_outreach_coaching",
    velocity_score: 68.0, breadth_score: 75.0,
    responsiveness_score: 72.0, momentum_score: 65.0,
    engagement_composite: 71.0,
    has_engagement_gap: true, requires_engagement_coaching: true,
    estimated_pipeline_at_risk_usd: 1440000.0,
    engagement_signal: "Executive access deficit — 6.5d avg buyer response time — 1.2 avg stakeholders — 3.5 ghosting episodes/deal — composite 71",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    engagement_risk: "critical", engagement_pattern: "executive_access_deficit",
    engagement_severity: "stalled", recommended_action: "executive_outreach_coaching",
    velocity_score: 100.0, breadth_score: 100.0,
    responsiveness_score: 100.0, momentum_score: 100.0,
    engagement_composite: 100.0,
    has_engagement_gap: true, requires_engagement_coaching: true,
    estimated_pipeline_at_risk_usd: 2400000.0,
    engagement_signal: "Executive access deficit — 7.0d avg buyer response time — 1.2 avg stakeholders — 4.0 ghosting episodes/deal — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-buyer-engagement-velocity-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.engagement_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.engagement_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_vel = 0, total_bre = 0, total_res = 0, total_mom = 0, total_loss = 0;

  for (const r of mockReps) {
    risk_counts[r.engagement_risk]         = (risk_counts[r.engagement_risk] || 0) + 1;
    pattern_counts[r.engagement_pattern]   = (pattern_counts[r.engagement_pattern] || 0) + 1;
    severity_counts[r.engagement_severity] = (severity_counts[r.engagement_severity] || 0) + 1;
    action_counts[r.recommended_action]    = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.engagement_composite;
    total_vel  += r.velocity_score;
    total_bre  += r.breadth_score;
    total_res  += r.responsiveness_score;
    total_mom  += r.momentum_score;
    total_loss += r.estimated_pipeline_at_risk_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                                     n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_engagement_composite:                  Math.round((total_comp / n) * 10) / 10,
      engagement_gap_count:                      mockReps.filter((r) => r.has_engagement_gap).length,
      coaching_count:                            mockReps.filter((r) => r.requires_engagement_coaching).length,
      avg_velocity_score:                        Math.round((total_vel / n) * 10) / 10,
      avg_breadth_score:                         Math.round((total_bre / n) * 10) / 10,
      avg_responsiveness_score:                  Math.round((total_res / n) * 10) / 10,
      avg_momentum_score:                        Math.round((total_mom / n) * 10) / 10,
      total_estimated_pipeline_at_risk_usd:      Math.round(total_loss * 100) / 100,
    },
  });
}
