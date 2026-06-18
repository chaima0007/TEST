import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    relationship_risk: "low", relationship_pattern: "none",
    relationship_severity: "healthy", recommended_action: "no_action",
    engagement_frequency_score: 0.0, relationship_quality_score: 0.0,
    account_health_score: 0.0, strategic_depth_score: 0.0,
    relationship_health_composite: 0.0, is_relationship_at_risk: false,
    requires_csa_intervention: false, estimated_revenue_at_risk_usd: 0.0,
    relationship_signal: "Customer relationship health strong across portfolio",
  },
  {
    rep_id: "rep_002", region: "East",
    relationship_risk: "low", relationship_pattern: "none",
    relationship_severity: "healthy", recommended_action: "no_action",
    engagement_frequency_score: 8.0, relationship_quality_score: 10.0,
    account_health_score: 5.0, strategic_depth_score: 10.0,
    relationship_health_composite: 8.0, is_relationship_at_risk: false,
    requires_csa_intervention: false, estimated_revenue_at_risk_usd: 0.0,
    relationship_signal: "Customer relationship health strong across portfolio",
  },
  {
    rep_id: "rep_003", region: "Central",
    relationship_risk: "moderate", relationship_pattern: "qbr_backlog",
    relationship_severity: "at_risk", recommended_action: "proactive_outreach",
    engagement_frequency_score: 38.0, relationship_quality_score: 10.0,
    account_health_score: 8.0, strategic_depth_score: 20.0,
    relationship_health_composite: 20.0, is_relationship_at_risk: false,
    requires_csa_intervention: false, estimated_revenue_at_risk_usd: 0.0,
    relationship_signal: "Qbr backlog — 3 QBRs overdue — composite 20",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    relationship_risk: "moderate", relationship_pattern: "expansion_neglect",
    relationship_severity: "at_risk", recommended_action: "proactive_outreach",
    engagement_frequency_score: 20.0, relationship_quality_score: 10.0,
    account_health_score: 8.0, strategic_depth_score: 35.0,
    relationship_health_composite: 19.0, is_relationship_at_risk: false,
    requires_csa_intervention: false, estimated_revenue_at_risk_usd: 0.0,
    relationship_signal: "Expansion neglect — 1 NPS declining accounts — composite 21",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    relationship_risk: "high", relationship_pattern: "executive_neglect",
    relationship_severity: "degrading", recommended_action: "executive_engagement_push",
    engagement_frequency_score: 55.0, relationship_quality_score: 25.0,
    account_health_score: 20.0, strategic_depth_score: 35.0,
    relationship_health_composite: 35.0, is_relationship_at_risk: false,
    requires_csa_intervention: false, estimated_revenue_at_risk_usd: 24000.0,
    relationship_signal: "Executive neglect — 2 NPS declining accounts — 2 usage declining — composite 44",
  },
  {
    rep_id: "rep_006", region: "West",
    relationship_risk: "high", relationship_pattern: "relationship_decay",
    relationship_severity: "degrading", recommended_action: "account_health_review",
    engagement_frequency_score: 20.0, relationship_quality_score: 47.0,
    account_health_score: 35.0, strategic_depth_score: 20.0,
    relationship_health_composite: 33.0, is_relationship_at_risk: true,
    requires_csa_intervention: true, estimated_revenue_at_risk_usd: 40000.0,
    relationship_signal: "Relationship decay — 3 NPS declining accounts — 3 usage declining — 3 escalations — composite 43",
  },
  {
    rep_id: "rep_007", region: "APAC",
    relationship_risk: "critical", relationship_pattern: "account_health_crisis",
    relationship_severity: "critical", recommended_action: "customer_success_emergency",
    engagement_frequency_score: 55.0, relationship_quality_score: 60.0,
    account_health_score: 65.0, strategic_depth_score: 50.0,
    relationship_health_composite: 58.0, is_relationship_at_risk: true,
    requires_csa_intervention: true, estimated_revenue_at_risk_usd: 90000.0,
    relationship_signal: "Account health crisis — 4 NPS declining accounts — 5 usage declining — 5 escalations — composite 62",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    relationship_risk: "critical", relationship_pattern: "relationship_decay",
    relationship_severity: "critical", recommended_action: "executive_intervention",
    engagement_frequency_score: 75.0, relationship_quality_score: 80.0,
    account_health_score: 75.0, strategic_depth_score: 65.0,
    relationship_health_composite: 75.0, is_relationship_at_risk: true,
    requires_csa_intervention: true, estimated_revenue_at_risk_usd: 200000.0,
    relationship_signal: "Relationship decay — 6 NPS declining accounts — 7 usage declining — 4 QBRs overdue — 7 escalations — composite 75",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-customer-relationship-health-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.relationship_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.relationship_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_freq = 0, total_qual = 0, total_hlth = 0, total_strat = 0, total_rev = 0;

  for (const r of mockReps) {
    risk_counts[r.relationship_risk]         = (risk_counts[r.relationship_risk] || 0) + 1;
    pattern_counts[r.relationship_pattern]   = (pattern_counts[r.relationship_pattern] || 0) + 1;
    severity_counts[r.relationship_severity] = (severity_counts[r.relationship_severity] || 0) + 1;
    action_counts[r.recommended_action]      = (action_counts[r.recommended_action] || 0) + 1;
    total_comp  += r.relationship_health_composite;
    total_freq  += r.engagement_frequency_score;
    total_qual  += r.relationship_quality_score;
    total_hlth  += r.account_health_score;
    total_strat += r.strategic_depth_score;
    total_rev   += r.estimated_revenue_at_risk_usd;
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
      avg_relationship_health_composite:    Math.round((total_comp / n) * 10) / 10,
      relationship_at_risk_count:           mockReps.filter((r) => r.is_relationship_at_risk).length,
      csa_intervention_count:               mockReps.filter((r) => r.requires_csa_intervention).length,
      avg_engagement_frequency_score:       Math.round((total_freq / n) * 10) / 10,
      avg_relationship_quality_score:       Math.round((total_qual / n) * 10) / 10,
      avg_account_health_score:             Math.round((total_hlth / n) * 10) / 10,
      avg_strategic_depth_score:            Math.round((total_strat / n) * 10) / 10,
      total_estimated_revenue_at_risk_usd:  Math.round(total_rev * 100) / 100,
    },
  });
}
