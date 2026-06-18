import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockCustomers = [
  {
    customer_id: "cust_001", csm_id: "csm_001",
    erosion_risk: "low", erosion_pattern: "none",
    erosion_severity: "healthy", recommended_action: "no_action",
    usage_decline_score: 0.0, engagement_decay_score: 0.0,
    expansion_health_score: 0.0, relationship_risk_score: 0.0,
    erosion_composite: 0.0, is_at_churn_risk: false, requires_executive_attention: false,
    estimated_arr_at_risk_usd: 0.0,
    erosion_signal: "Customer health within acceptable parameters",
  },
  {
    customer_id: "cust_002", csm_id: "csm_001",
    erosion_risk: "low", erosion_pattern: "expansion_stall",
    erosion_severity: "healthy", recommended_action: "no_action",
    usage_decline_score: 6.0, engagement_decay_score: 5.0,
    expansion_health_score: 20.0, relationship_risk_score: 4.0,
    erosion_composite: 9.8, is_at_churn_risk: false, requires_executive_attention: false,
    estimated_arr_at_risk_usd: 9800.0,
    erosion_signal: "24mo customer — $0 expansion in 12m — 180d to renewal — composite 10",
  },
  {
    customer_id: "cust_003", csm_id: "csm_002",
    erosion_risk: "moderate", erosion_pattern: "usage_cliff",
    erosion_severity: "watch", recommended_action: "csm_outreach",
    usage_decline_score: 28.0, engagement_decay_score: 18.0,
    expansion_health_score: 12.0, relationship_risk_score: 8.0,
    erosion_composite: 18.8, is_at_churn_risk: false, requires_executive_attention: false,
    estimated_arr_at_risk_usd: 37600.0,
    erosion_signal: "Usage 60 vs 80 prior — adoption 45% — composite 19",
  },
  {
    customer_id: "cust_004", csm_id: "csm_002",
    erosion_risk: "moderate", erosion_pattern: "support_overload",
    erosion_severity: "watch", recommended_action: "csm_outreach",
    usage_decline_score: 14.0, engagement_decay_score: 40.0,
    expansion_health_score: 10.0, relationship_risk_score: 12.0,
    erosion_composite: 21.2, is_at_churn_risk: false, requires_executive_attention: false,
    estimated_arr_at_risk_usd: 42400.0,
    erosion_signal: "2 critical tickets — NPS 35 — composite 21",
  },
  {
    customer_id: "cust_005", csm_id: "csm_003",
    erosion_risk: "high", erosion_pattern: "exec_relationship_loss",
    erosion_severity: "degrading", recommended_action: "executive_qbr",
    usage_decline_score: 20.0, engagement_decay_score: 25.0,
    expansion_health_score: 22.0, relationship_risk_score: 55.0,
    erosion_composite: 28.5, is_at_churn_risk: false, requires_executive_attention: true,
    estimated_arr_at_risk_usd: 142500.0,
    erosion_signal: "Exec dark 75d — 1 meeting vs 4 prior — composite 29",
  },
  {
    customer_id: "cust_006", csm_id: "csm_003",
    erosion_risk: "high", erosion_pattern: "usage_cliff",
    erosion_severity: "degrading", recommended_action: "executive_qbr",
    usage_decline_score: 55.0, engagement_decay_score: 38.0,
    expansion_health_score: 30.0, relationship_risk_score: 18.0,
    erosion_composite: 39.2, is_at_churn_risk: false, requires_executive_attention: true,
    estimated_arr_at_risk_usd: 196000.0,
    erosion_signal: "Usage 30 vs 75 prior — adoption 20% — composite 39",
  },
  {
    customer_id: "cust_007", csm_id: "csm_004",
    erosion_risk: "critical", erosion_pattern: "competitive_migration",
    erosion_severity: "critical", recommended_action: "rescue_plan",
    usage_decline_score: 55.0, engagement_decay_score: 60.0,
    expansion_health_score: 50.0, relationship_risk_score: 65.0,
    erosion_composite: 57.5, is_at_churn_risk: true, requires_executive_attention: true,
    estimated_arr_at_risk_usd: 575000.0,
    erosion_signal: "Competitor evaluation active — exec dark 90d — composite 58",
  },
  {
    customer_id: "cust_008", csm_id: "csm_004",
    erosion_risk: "critical", erosion_pattern: "competitive_migration",
    erosion_severity: "critical", recommended_action: "churn_prevention_team",
    usage_decline_score: 80.0, engagement_decay_score: 75.0,
    expansion_health_score: 70.0, relationship_risk_score: 80.0,
    erosion_composite: 76.3, is_at_churn_risk: true, requires_executive_attention: true,
    estimated_arr_at_risk_usd: 1526000.0,
    erosion_signal: "Competitor evaluation active — exec dark 120d — composite 76",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/customer-ltv-erosion-detector`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let customers = [...mockCustomers];
  if (risk)    customers = customers.filter((c) => c.erosion_risk    === risk);
  if (pattern) customers = customers.filter((c) => c.erosion_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_usg = 0, total_eng = 0, total_exp = 0, total_rel = 0;
  let total_arr = 0;

  for (const c of mockCustomers) {
    risk_counts[c.erosion_risk]       = (risk_counts[c.erosion_risk] || 0) + 1;
    pattern_counts[c.erosion_pattern] = (pattern_counts[c.erosion_pattern] || 0) + 1;
    severity_counts[c.erosion_severity] = (severity_counts[c.erosion_severity] || 0) + 1;
    action_counts[c.recommended_action] = (action_counts[c.recommended_action] || 0) + 1;
    total_comp += c.erosion_composite;
    total_usg  += c.usage_decline_score;
    total_eng  += c.engagement_decay_score;
    total_exp  += c.expansion_health_score;
    total_rel  += c.relationship_risk_score;
    total_arr  += c.estimated_arr_at_risk_usd;
  }

  const n = mockCustomers.length;

  return NextResponse.json({
    customers,
    summary: {
      total:                            n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_erosion_composite:            Math.round((total_comp / n) * 10) / 10,
      churn_risk_count:                 mockCustomers.filter((c) => c.is_at_churn_risk).length,
      executive_attention_count:        mockCustomers.filter((c) => c.requires_executive_attention).length,
      avg_usage_decline_score:          Math.round((total_usg  / n) * 10) / 10,
      avg_engagement_decay_score:       Math.round((total_eng  / n) * 10) / 10,
      avg_expansion_health_score:       Math.round((total_exp  / n) * 10) / 10,
      avg_relationship_risk_score:      Math.round((total_rel  / n) * 10) / 10,
      total_estimated_arr_at_risk_usd:  Math.round(total_arr * 100) / 100,
    },
  });
}
